import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
const modules = 'C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1026-487-0_26.1026.487.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules';
const require = createRequire(path.join(modules, '../runtime.cjs'));
const { FileBlob, SpreadsheetFile } = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const work = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(work, '../..');
const target = path.join(root, 'Go Live Files/Edited/Stock Import/Stock Import - Client Review.xlsx');
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(target));
if (process.argv.includes('--verify-workflow')) {
  console.log((await wb.inspect({kind:'workbook,sheet,table',maxChars:2000,tableMaxRows:2,tableMaxCols:7})).ndjson);
  const names=[0,1].map(i=>wb.worksheets.getItemAt(i).name);
  if(JSON.stringify(names)!==JSON.stringify(['Client review','Excluded'])) throw new Error('Wrong sheets');
  if(wb.worksheets.getItem('Client review').getRange('E1:G1').values[0].join('|')!=='Final internal reference|Quantity to import|Notes / changes needed') throw new Error('Wrong response fields');
  console.log('Saved workbook imported and verified.');
  process.exit(0);
}
if (process.argv.includes('--workflow')) {
  const client = wb.worksheets.getItem('Client review');
  const before = client.getRange('A2:H12').values;
  const excluded = wb.worksheets.getItem('Excluded').getRange('A1:E2').values;
  const notes = r => [r[5],r[2] == null ? null : `Counted as: ${r[2]}`].filter(x=>x!=null && x!=='').join('\n') || null;
  const rows = before.map(r=>[r[0],r[1],r[3],r[4],r[6],r[7],notes(r)]);
  await fs.writeFile(path.join(work,'workflow-before.json'),JSON.stringify({rows:before,excluded},null,2));
  client.tables.items[0].delete();
  client.getRange('A15:H17').unmerge();
  client.getRange('A1:H17').clear({applyTo:'all'});
  const headers = ['Current internal reference','Product on stocktake','Stocktake quantity','What to check','Final internal reference','Quantity to import','Notes / changes needed'];
  client.getRange('A1:G12').values = [headers,...rows];
  const table = client.tables.add('A1:G12',true,'ClientreviewTable');
  table.style = 'TableStyleLight1';
  table.showFilterButton = true;
  client.getRange('A1:G12').format = {font:{name:'Arial',size:11,color:'#253649'},fill:'#FFFFFF',verticalAlignment:'center',wrapText:true};
  client.getRange('A1:G1').format = {fill:'#24476A',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},rowHeight:42,horizontalAlignment:'center',verticalAlignment:'center',wrapText:true};
  client.getRange('D1').format.fill = '#714B67';
  client.getRange('E1:G1').format = {fill:'#E7B34B',font:{name:'Arial',size:11,bold:true,color:'#253649'}};
  client.getRange('E2:G12').format.fill = '#FFF5D9';
  client.getRange('A2:G12').format.rowHeight = 78;
  const widths=[23,40,19,61,24,20,48];
  widths.forEach((width,i)=>client.getRange(`${String.fromCharCode(65+i)}1:${String.fromCharCode(65+i)}17`).format.columnWidth=width);
  client.getRange('A2:A12').setNumberFormat('@');
  client.getRange('E2:E12').setNumberFormat('@');
  client.getRange('C2:C12').setNumberFormat('0.########');
  client.getRange('F2:F12').setNumberFormat('0.########');
  client.getRange('C2:C12').format.horizontalAlignment='right';
  client.getRange('F2:F12').format.horizontalAlignment='right';
  client.getRange('F2:F12').dataValidation={rule:{type:'decimal',operator:'greaterThanOrEqual',formula1:0}};
  client.mergeCells('A15:G17');
  client.getRange('A15').values=[["Look up each current reference in Odoo. Either update the product references there, or explain the changes needed in Notes. Fill in Final internal reference and Quantity to import. Before import, each final reference must identify one product in Odoo. In Notes, identify the chosen product (add its Odoo link if names are identical), say whether you counted cartons, packs or items, and list each product's reference and quantity if the count needs splitting. Leave unchecked quantities blank; enter 0 only for no stock. Original quantities are from your 1 Oct stocktake. MISC is on Excluded."]];
  client.getRange('A15:G17').format={font:{name:'Arial',size:11,color:'#253649'},fill:'#FFF5D9',wrapText:true,verticalAlignment:'center',rowHeight:30};
  wb.recalculate();
  if (JSON.stringify(client.getRange('A2:C12').values)!==JSON.stringify(before.map(r=>[r[0],r[1],r[3]]))) throw new Error('Source values changed');
  if (JSON.stringify(wb.worksheets.getItem('Excluded').getRange('A1:E2').values)!==JSON.stringify(excluded)) throw new Error('Excluded changed');
  console.log((await wb.inspect({kind:'table',range:"'Client review'!A1:G4",include:'values,formulas',tableMaxRows:4,tableMaxCols:7,maxChars:1800})).ndjson);
  console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:800})).ndjson);
  for(const [range,name] of [['A1:G12','table'],['A15:G17','instructions']]) {
    const blob=await wb.render({sheetName:'Client review',range,scale:1.2,format:'png'});
    await fs.writeFile(path.join(work,`workflow-${name}.png`),new Uint8Array(await blob.arrayBuffer()));
  }
  const stage=path.join(work,'workflow-stage.xlsx');
  await (await SpreadsheetFile.exportXlsx(wb)).save(stage);
  console.log('Staged workflow: '+stage);
  process.exit(0);
}
if (process.argv.includes('--edit')) {
  const client = wb.worksheets.getItem('Client review');
  const matches = wb.worksheets.getItem('Product matches');
  const excluded = wb.worksheets.getItem('Excluded');
  const originalClient = client.getRange('A2:H12').values;
  const originalMatches = matches.getRange('A2:C23').values;
  const originalExcluded = excluded.getRange('A2:D2').values;
  const questions = {
    BDT80: 'There are two products with this code. One name ends in NEW. Which product does the count of 55 belong to? If both were counted, tell us the quantity for each.',
    BFH130: 'There are two Flump Hearts products with this code. One name ends in NEW PRODUCT. Which one was counted?',
    BFS120: 'This code is used for Fruity Mix and Squishy Sunburst. Which product was counted?',
    BT03: 'There are two Master Blend products with this code. One name ends in NEW PRODUCT. Which one was counted? Please also check the count of 20.33 and say whether it means cartons, packs or individual items.',
    CM05: 'This code is used for both 48x49g and 48x54g Mint Crisp. The stocktake says 48x49g. Which pack size was counted?',
    CO07S: 'There are two Odoo products with the same code and name. Please ask Veer to help identify which one the count belongs to.',
    EC03: 'There are two Odoo products with the same code and name. Please ask Veer to help identify which one the count belongs to.',
    GC01: 'This code is used for both 48x49g and 48x54g Golden Crisp. The stocktake says 48x54g. Which pack size was counted?',
    LFG130: 'There are two Football Gums products with this code. One name ends in BAG. Which one was counted? Were you counting cartons, bags or individual items?',
    LLG130: 'There are two Liquorice Gums products with this code. One name ends in BAG. Which one was counted? Were you counting cartons, bags or individual items?',
    LMG130: 'This code is used for Midget Gems BAG and Mini Gems. Which product was counted?'
  };
  client.getRange('A1:H1').values = [['Product code','Product on stocktake','Counted as','Stocktake quantity','What to check','Your answer / product chosen','Product code to use','Quantity to use']];
  client.getRange('E2:E12').values = originalClient.map(r=>[questions[r[0]]]);
  client.getRange('A15:H16').unmerge();
  client.getRange('A15:H16').clear({applyTo:'contents'});
  client.mergeCells('A15:H17');
  client.getRange('A15').values = [["These 11 items still need your confirmation. Compare the choices on Product matches and fill in the yellow answer columns. Quantities come from your original 1 Oct stocktake. Please say whether you counted cartons, packs or individual items in Counted as. Leave Quantity to use blank until checked. Enter 0 only if there is no stock. Tell Veer how to split the quantity if both products were counted. MISC is listed on Excluded."]];
  client.getRange('A15:H17').format = {font:{name:'Arial',size:11,color:'#253649'},fill:'#FFF5D9',wrapText:true,verticalAlignment:'center',rowHeight:24};
  // Retain the existing blank unit fields as an obvious place to confirm counted units.
  client.getRange('C1').format = {fill:'#E7B34B',font:{name:'Arial',size:11,bold:true,color:'#253649'}};
  client.getRange('C2:C12').format.fill = '#FFF5D9';
  // Remove the two internal tracing columns while preserving the other candidate data.
  matches.tables.items[0].delete();
  matches.getRange('A26:E27').unmerge();
  matches.getRange('D1:E27').clear({applyTo:'all'});
  matches.getRange('A26:C27').clear({applyTo:'contents'});
  matches.getRange('A1:C1').values = [['Product code','Product name in Odoo','Odoo product ID']];
  const table = matches.tables.add('A1:C23', true, 'ProductmatchesTable');
  table.style = 'TableStyleLight1';
  table.showFilterButton = true;
  matches.mergeCells('A26:C28');
  matches.getRange('A26').values = [["Each code has two possible products. Compare the name and pack size, then enter your choice on Client review. The Odoo product ID helps Veer tell identical names apart. These names come from the earlier product list. NEW or BAG in a name does not tell us which product was counted."]];
  matches.getRange('A26:C28').format = {font:{name:'Arial',size:11,color:'#253649'},fill:'#FFF5D9',wrapText:true,verticalAlignment:'center',rowHeight:24};
  excluded.getRange('A1:E1').values = [['Product code','Product on stocktake','Counted as','Stocktake quantity','Why left out']];
  excluded.getRange('E2').values = [["Left out of the import at Nitin's request. The stocktake quantity of 15 is kept here for reference."]];
  for (const [sheet,range] of [[client,'A1:H12'],[excluded,'A1:E2']]) {
    const previousTable = sheet.tables.items[0];
    const name = previousTable.name;
    previousTable.delete();
    const updatedTable = sheet.tables.add(range,true,name);
    updatedTable.style = 'TableStyleLight1';
    updatedTable.showFilterButton = true;
  }
  wb.recalculate();
  function same(a,b,label) { if(JSON.stringify(a)!==JSON.stringify(b)) throw new Error('Unexpected change: '+label); }
  same(client.getRange('A2:D12').values,originalClient.map(r=>r.slice(0,4)),'source stocktake rows');
  same(client.getRange('F2:H12').values,originalClient.map(r=>r.slice(5,8)),'client responses');
  same(matches.getRange('A2:C23').values,originalMatches,'22 candidate identities');
  same(excluded.getRange('A2:D2').values,originalExcluded,'excluded count');
  for(const name of ['Client review','Product matches','Excluded']) {
    console.log((await wb.inspect({kind:'table',range:`'${name}'!A1:${name==='Client review'?'H4':name==='Product matches'?'C4':'E2'}`,include:'values,formulas',tableMaxRows:4,tableMaxCols:8,maxChars:2500})).ndjson);
  }
  console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:20},maxChars:1000})).ndjson);
  for (const [name,range,suffix] of [['Client review','A1:H12','table'],['Client review','A15:H17','note'],['Product matches','A1:C23','table'],['Product matches','A26:C28','note'],['Excluded','A1:E2','table']]) {
    const blob = await wb.render({sheetName:name,range,scale:1.25,format:'png'});
    await fs.writeFile(path.join(work,`after-${name.replaceAll(' ','-')}-${suffix}.png`),new Uint8Array(await blob.arrayBuffer()));
  }
  const stagedDir = path.join(root,'Output/outputs/2026-11-02-stock-review');
  await fs.mkdir(stagedDir,{recursive:true});
  const staged = path.join(stagedDir,'Stock Import - Client Review.xlsx');
  await (await SpreadsheetFile.exportXlsx(wb)).save(staged);
  let delivered = target;
  try { await fs.copyFile(staged,target); await fs.unlink(staged); }
  catch(error) { delivered=staged; console.log('Original workbook could not be replaced: '+error.code); }
  await fs.writeFile(path.join(work,'simplify-review-result.json'),JSON.stringify({delivered,reviewLines:11,candidates:22,reviewQuantity:originalClient.reduce((s,r)=>s+r[3],0),excludedQuantity:originalExcluded[0][3]},null,2));
  console.log('Saved: '+delivered);
  process.exit(0);
}
console.log((await wb.inspect({kind:'workbook,sheet,table',maxChars:3500,tableMaxRows:2,tableMaxCols:8})).ndjson);
for (const name of ['Client review','Product matches','Excluded']) {
  const sheet = wb.worksheets.getItem(name);
  console.log(name, JSON.stringify(sheet.getUsedRange().values));
  const preview = await wb.render({sheetName:name,range:name==='Client review'?'A1:H4':name==='Product matches'?'A1:E5':'A1:E2',scale:1,format:'png'});
  await fs.writeFile(path.join(work, `before-${name.replaceAll(' ','-')}.png`),new Uint8Array(await preview.arrayBuffer()));
}
console.log(wb.help('*', {search:'worksheets.delete|worksheets.remove|worksheet.delete|worksheet.remove',include:'index,notes,examples',maxChars:3600}).ndjson);
