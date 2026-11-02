import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL, fileURLToPath} from 'node:url';

const work = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(work, '../..');
const modules = 'C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1026-487-0_26.1026.487.0_x64__3k8sg7r9htsxt/dependencies/node/node_modules';
const require = createRequire(path.join(modules, '../runtime.cjs'));
const {Workbook, SpreadsheetFile, FileBlob} = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const data = JSON.parse(await fs.readFile(path.join(work, 'data.json'), 'utf8'));
const out = path.join(root, 'Go Live Files/Edited/Stock Import');
await fs.mkdir(out, {recursive: true});

const C = {navy:'#24476A', purple:'#714B67', amber:'#E7B34B', pale:'#FFF5D9', ink:'#253649', white:'#FFFFFF'};
const files = [];
function lastCol(count) { return String.fromCharCode(64 + count); }
function createSheet(wb, name, headers, rows, widths, amber=[], purple=[]) {
  const sheet = wb.worksheets.add(name);
  const end = rows.length + 1;
  const col = lastCol(headers.length);
  const full = `A1:${col}${end}`;
  sheet.showGridLines = false;
  sheet.tabColor = name === 'Client review' ? C.amber : name === 'Product matches' ? C.purple : C.navy;
  sheet.getRange(full).values = [headers, ...rows];
  const table = sheet.tables.add(full, true, name.replaceAll(' ', '') + 'Table');
  table.style = 'TableStyleLight1';
  table.showFilterButton = true;
  sheet.getRange(full).format = {font:{name:'Arial', size:11, color:C.ink}, fill:C.white,
    verticalAlignment:'center', rowHeight:24};
  sheet.getRange(`A1:${col}1`).format = {fill:C.navy,
    font:{name:'Arial',size:11,bold:true,color:C.white}, rowHeight:36,
    horizontalAlignment:'center', verticalAlignment:'center', wrapText:true};
  for (let i = 0; i < widths.length; i++) {
    const letter = lastCol(i + 1);
    sheet.getRange(`${letter}1:${letter}${end}`).format.columnWidth = widths[i];
  }
  for (const letter of purple) sheet.getRange(`${letter}1`).format.fill = C.purple;
  for (const letter of amber) {
    sheet.getRange(`${letter}1`).format.fill = C.amber;
    sheet.getRange(`${letter}1`).format.font.color = C.ink;
    sheet.getRange(`${letter}2:${letter}${end}`).format.fill = C.pale;
  }
  sheet.getRange(`A2:A${end}`).setNumberFormat('@');
  sheet.freezePanes.freezeRows(1);
  return sheet;
}
function quantity(sheet, range, validate=false) {
  sheet.getRange(range).setNumberFormat('0.########');
  if (validate) sheet.getRange(range).dataValidation = {rule:{type:'decimal', operator:'greaterThanOrEqual', formula1:0}};
}
async function render(wb, name, range, file, scale=1.25) {
  const preview = await wb.render({sheetName:name, range, scale, format:'png'});
  await fs.writeFile(path.join(work, file), new Uint8Array(await preview.arrayBuffer()));
}
async function check(wb, sheet, range) {
  console.log((await wb.inspect({kind:'table', range:`'${sheet}'!${range}`, include:'values,formulas',
    tableMaxRows:4, tableMaxCols:8, maxChars:1800})).ndjson);
  const errors = await wb.inspect({kind:'match', searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',
    options:{useRegex:true,maxResults:20}, maxChars:1200});
  console.log(errors.ndjson);
}

// The unchanged reference palette and layout were verified during initial creation.

const ready = Workbook.create();
const importSheet = createSheet(ready, 'Import', ['Product', 'Counted'],
  data.ready.map(r => [r[0],r[3]]), [24,22], ['B']);
quantity(importSheet, `B2:B${data.ready.length+1}`);
const list = createSheet(ready, 'Product list',
  ['Internal Reference','Product / Variant','Unit of Measure','Counted Quantity','Notes'],
  data.ready, [19,50,17,20,54], ['D','E']);
list.getRange(`B2:B${data.ready.length+1}`).format.wrapText = true;
list.getRange(`E2:E${data.ready.length+1}`).format.wrapText = true;
list.getRange(`A2:E${data.ready.length+1}`).format.rowHeight = 34;
quantity(list, `D2:D${data.ready.length+1}`);
const readyNoteRow = data.ready.length + 4;
list.mergeCells(`A${readyNoteRow}:E${readyNoteRow+2}`);
list.getRange(`A${readyNoteRow}:E${readyNoteRow+2}`).values = [[
  'Quantity source: client-supplied UK_Central_Wholesale_-_Stocktake_1_Oct_2026.xlsx, Stocktake. Source units are blank and unconfirmed. Counts are preserved without conversion or rounding; Odoo interprets them in each product\'s configured inventory unit. Run Odoo Test before import.'
]];
list.getRange(`A${readyNoteRow}:E${readyNoteRow+2}`).format = {font:{name:'Arial',size:11,color:C.ink},fill:C.pale,wrapText:true,rowHeight:24,verticalAlignment:'center'};
ready.recalculate();
await check(ready, 'Import', 'A1:B5');
await render(ready, 'Import', 'A1:B13', 'import-preview.png', 1.5);
await render(ready, 'Product list', 'A1:E10', 'product-list-preview.png');
const readyPath = path.join(out, 'Stock Import - Ready.xlsx');
await (await SpreadsheetFile.exportXlsx(ready)).save(readyPath);
files.push(readyPath);

const review = Workbook.create();
const reviewRows = data.review.map(r => [r.code, r.description, r.unit, r.quantity, r.issue, null, null, null]);
const client = createSheet(review, 'Client review',
  ['Internal Reference','Product / Variant','Unit of Measure','Counted Quantity','Issue to resolve',
   'Client decision / action','Confirmed Internal Reference','Confirmed Quantity'],
  reviewRows, [19,40,17,20,64,46,25,20], ['D','F','G','H'], ['E']);
client.getRange(`A2:H${reviewRows.length+1}`).format.wrapText = true;
client.getRange(`A2:H${reviewRows.length+1}`).format.rowHeight = 90;
quantity(client, `D2:D${reviewRows.length+1}`);
quantity(client, `H2:H${reviewRows.length+1}`, true);
client.getRange(`G2:G${reviewRows.length+1}`).setNumberFormat('@');
const noteRow = reviewRows.length + 4;
client.mergeCells(`A${noteRow}:H${noteRow+1}`);
client.getRange(`A${noteRow}:H${noteRow+1}`).values = [[
  `Quantity source: original client-supplied 1 Oct stocktake, not the last-cost workbook. Source units are blank and unconfirmed. Resolve the ${reviewRows.length} duplicate-reference lines using Product matches, then complete the response fields. MISC is separately excluded on the Excluded tab. Leave confirmed counts blank until agreed; 0 is an explicit nil count.`
]];
client.getRange(`A${noteRow}:H${noteRow+1}`).format = {font:{name:'Arial',size:11,color:C.ink},
  fill:C.pale,wrapText:true,verticalAlignment:'center',rowHeight:24};

const matches = data.review.flatMap(r => r.candidates.map(c => [r.code,c.name,c.templateId,
  r.selectedTemplateId === c.templateId ? 'Yes - previous lookup' : r.selectedTemplateId ? 'No' : 'No previous lookup', c.sourceRow]));
const candidates = createSheet(review, 'Product matches',
  ['Internal Reference','Exported Product Name','Product Template ID','Selected in previous lookup','Export Sheet Row'],
  matches, [19,78,24,29,19], [], ['B','C','D','E']);
candidates.getRange(`B2:B${matches.length+1}`).format.wrapText = true;
candidates.getRange(`A2:E${matches.length+1}`).format.rowHeight = 36;
candidates.getRange(`C2:C${matches.length+1}`).setNumberFormat('@');
const matchNoteRow = matches.length + 4;
candidates.mergeCells(`A${matchNoteRow}:E${matchNoteRow+1}`);
candidates.getRange(`A${matchNoteRow}:E${matchNoteRow+1}`).values = [[
  'Historical product export supplied before the cost update. Template IDs are for investigation only. The edited last-cost workbook\'s VLOOKUP selects the first matching reference; it does not confirm the correct product. NEW and BAG suffixes do not establish which record is correct.'
]];
candidates.getRange(`A${matchNoteRow}:E${matchNoteRow+1}`).format = {font:{name:'Arial',size:11,color:C.ink},
  fill:C.pale,wrapText:true,verticalAlignment:'center',rowHeight:28};
const excludedSheet = createSheet(review, 'Excluded',
  ['Internal Reference','Product / Variant','Unit of Measure','Source Quantity','Reason for exclusion'],
  data.excluded.map(r=>[r.code,r.description,r.unit,r.quantity,r.reason]), [19,40,17,20,80], ['D'], ['E']);
excludedSheet.getRange('A2:E2').format.wrapText = true;
excludedSheet.getRange('A2:E2').format.rowHeight = 72;
quantity(excludedSheet, 'D2:D2');
review.recalculate();
await check(review, 'Client review', 'A1:H4');
await render(review, 'Client review', 'A1:H6', 'client-review-preview.png', 1);
await render(review, 'Product matches', 'A1:E12', 'matches-preview.png', 1.15);
await render(review, 'Excluded', 'A1:E2', 'excluded-preview.png', 1.15);
const reviewPath = path.join(out, 'Stock Import - Client Review.xlsx');
await (await SpreadsheetFile.exportXlsx(review)).save(reviewPath);
files.push(reviewPath);
await fs.writeFile(path.join(work, 'outputs.json'), JSON.stringify({files, readyCount:data.ready.length,
  reviewCount:data.review.length, excludedCount:data.excluded.length, sourceCount:data.sourceCount}, null, 2));
console.log(JSON.stringify({files,readyCount:data.ready.length,reviewCount:data.review.length,excludedCount:data.excluded.length}));
