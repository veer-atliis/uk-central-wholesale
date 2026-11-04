import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const modules='C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1103-91-0_26.1103.91.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules';
const require=createRequire(path.join(modules,'../runtime.cjs'));
const {Workbook,SpreadsheetFile,FileBlob}=await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const work=path.resolve('Working Files/2026-11-05 Stock Import');
const out=path.resolve('Go Live Files/Edited/Stock Import');
const d=JSON.parse(await fs.readFile(path.join(work,'data.json'),'utf8'));
const reviewPath=path.join(out,'Stock Import - Client Review.xlsx');
const review=await SpreadsheetFile.importXlsx(await FileBlob.load(reviewPath));
await fs.copyFile(reviewPath,path.join(work,'Client Review - before.xlsx'));
await fs.writeFile(path.join(work,'review-before.png'),new Uint8Array(await (await review.render({sheetName:'Client review',range:'A1:G4',scale:1,format:'png'})).arrayBuffer()));
if(process.argv.includes('--before')) process.exit(0);
function sheet(wb,name,rows,widths){
 const s=wb.worksheets.add(name), end=rows.length, col=String.fromCharCode(64+rows[0].length), range=`A1:${col}${end}`;
 s.showGridLines=false;s.getRange(range).values=rows;
 s.getRange(range).format={font:{name:'Arial',size:11,color:'#253649'},verticalAlignment:'center',rowHeight:26,wrapText:true};
 s.getRange(`A1:${col}1`).format={fill:'#24476A',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},rowHeight:40,wrapText:true};
 widths.forEach((w,i)=>s.getRange(`${String.fromCharCode(65+i)}1:${String.fromCharCode(65+i)}${end}`).format.columnWidth=w);
 s.getRange(`A2:A${end}`).setNumberFormat('@');s.freezePanes.freezeRows(1);
 const t=s.tables.add(range,true,name.replaceAll(' ','')+'Table');t.style='TableStyleLight1';return s;
}
const ready=Workbook.create();
sheet(ready,'Import',[['Product','Counted'],...d.ready.map(r=>[r[0],r[3]])],[24,22]).getRange('B2:B10').setNumberFormat('0.########');
sheet(ready,'Product list',[['Internal Reference','Product / Variant','Unit of Measure','Counted Quantity','Notes'],...d.ready],[24,48,22,22,40]).getRange('D2:D10').setNumberFormat('0.########');
const s=review.worksheets.getItem('Client review');
for(const t of [...s.tables.items])t.delete();
s.getRange('A15:G17').unmerge();s.getRange('A1:G17').clear({applyTo:'all'});
const rows=d.held.map(r=>[r[0],r[1],r[3],r[0]==='BFH130'?'Cost is $0 in Odoo. This reference is absent from the supplied last-cost workbook. Please provide the correct cost (ex GST) and confirm the counted unit.':'Cost is $0 in Odoo. The supplied last-cost workbook includes this reference but has no last cost: No purchase in MYOB since 2020 - no last cost. Please provide the correct cost (ex GST) and confirm the counted unit.',null,null,null]);
s.getRange('A1:G3').values=[d.reviewBefore[0],...rows];
s.tables.add('A1:G3',true,'ClientreviewTable').style='TableStyleLight1';
s.getRange('A1:G3').format={font:{name:'Arial',size:11,color:'#253649'},fill:'#FFFFFF',wrapText:true,verticalAlignment:'center',rowHeight:115};
s.getRange('A1:G1').format={fill:'#24476A',font:{name:'Arial',size:11,bold:true,color:'#FFFFFF'},rowHeight:42,wrapText:true};
[23,40,19,61,24,20,48].forEach((w,i)=>s.getRange(`${String.fromCharCode(65+i)}1:${String.fromCharCode(65+i)}17`).format.columnWidth=w);
s.getRange('E1:G1').format.fill='#E7B34B';s.getRange('E1:G1').format.font.color='#253649';s.getRange('E2:G3').format.fill='#FFF5D9';
s.getRange('C2:C3').setNumberFormat('0.########');s.getRange('F2:F3').setNumberFormat('0.########');s.getRange('A2:A3').setNumberFormat('@');s.getRange('E2:E3').setNumberFormat('@');
s.mergeCells('A6:G8');s.getRange('A6').values=[['These two products are held from Stock Import - Ready 2 pending costs. Provide the cost excluding GST in Notes / changes needed, confirm the counted unit, and complete Final internal reference and Quantity to import after review. Original stocktake quantities are preserved; no cost has been assumed. MISC remains on Excluded.']];
s.getRange('A6:G8').format={font:{name:'Arial',size:11,color:'#253649'},fill:'#FFF5D9',wrapText:true,rowHeight:28,verticalAlignment:'center'};
for(const [wb,label,views] of [[ready,'ready2',[['Import','A1:B10'],['Product list','A1:E10']]],[review,'review',[['Client review','A1:G8'],['Excluded','A1:E2']]]]){
 wb.recalculate();
 for(const [name,range]of views)await fs.writeFile(path.join(work,`${label}-${name.replaceAll(' ','-')}.png`),new Uint8Array(await(await wb.render({sheetName:name,range,scale:1.1,format:'png'})).arrayBuffer()));
 console.log((await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:10},maxChars:500})).ndjson);
 await(await SpreadsheetFile.exportXlsx(wb)).save(path.join(work,label+'.xlsx'));
}
console.log('Staged ready2.xlsx and review.xlsx');
