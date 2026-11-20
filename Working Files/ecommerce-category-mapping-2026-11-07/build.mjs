import fs from 'node:fs/promises';
import {createRequire} from 'node:module';
import {pathToFileURL,fileURLToPath} from 'node:url';
const require = createRequire('C:/Program Files/WindowsApps/OpenAI.CodexPrimaryRuntime.v26-1104-2876-0_26.1104.2876.0_x64__3k8sg7r9htsxt/dependencies/node/package.json');
const {FileBlob,SpreadsheetFile} = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const dir = new URL('.',import.meta.url);
const sources = JSON.parse(await fs.readFile(new URL('sources.json',dir),'utf8'));
const products = sources['Product (product.template) (4).xlsx'].Sheet1;
const website = sources['Website Product Category (product.public.category).xlsx'].Sheet1.slice(1);
const internal = sources['Product Category (product.category) (6).xlsx'].Sheet1.slice(1);
const paths = new Set(internal.map(r=>r[2]));
const counts = {};
const mapped = products.slice(1).map((r,i)=>{
  if(!paths.has(r[6])) throw Error(`Unknown product category at row ${i+2}`);
  if(r[7] !== null) throw Error(`Existing ecommerce category at row ${i+2}`);
  const path = r[6].replace(/^UK Central Wholesale \/ /,'');
  const matches = website.filter(w=>w[3]===path);
  if(matches.length!==1) throw Error(`Ambiguous or missing category at row ${i+2}: ${path}`);
  counts[path]=(counts[path]||0)+1;
  return [matches[0][3]];
});
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load('C:/Users/veerm/Downloads/Product (product.template) (4).xlsx'));
const sheet=wb.worksheets.getItem('Sheet1');
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:1000})).ndjson);
const mode=process.argv[2]||'preview';
if(mode==='preview') {
 const blob=await wb.render({sheetName:'Sheet1',range:'F1:H8',scale:1.5,format:'png'});
 await fs.writeFile(new URL('before.png',dir),new Uint8Array(await blob.arrayBuffer()));
 console.log(JSON.stringify({products:mapped.length,counts}));
} else {
 sheet.getRange(`H2:H${products.length}`).values=mapped;
 wb.recalculate();
 const values=sheet.getRange(`A1:H${products.length}`).values;
 for(let r=0;r<products.length;r++) for(let c=0;c<8;c++) {
  const expected=r>0&&c===7?mapped[r-1][0]:products[r][c];
  if((values[r][c]??null)!==(expected??null)) throw Error(`Unexpected cell ${r+1},${c+1}`);
 }
 console.log((await wb.inspect({kind:'table',range:'Sheet1!G1:H8',include:'values,formulas',tableMaxRows:8,tableMaxCols:2,maxChars:3000})).ndjson);
 const blob=await wb.render({sheetName:'Sheet1',range:'F1:H8',scale:1.5,format:'png'});
 await fs.writeFile(new URL('after.png',dir),new Uint8Array(await blob.arrayBuffer()));
 const out=new URL('../../Output/outputs/ecommerce-category-mapping-2026-11-07/',dir);
 await fs.mkdir(out,{recursive:true});
 const file=await SpreadsheetFile.exportXlsx(wb);
 await file.save(fileURLToPath(new URL('Products - ecommerce categories populated.xlsx',out)));
 console.log(JSON.stringify({products:mapped.length,counts,validated:'All original cells outside H2:H129 unchanged'}));
}
