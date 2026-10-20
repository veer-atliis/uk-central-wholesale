import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
const require = createRequire('C:/Users/veerm/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/runtime.cjs');
const { FileBlob, SpreadsheetFile } = await import(pathToFileURL(require.resolve('@oai/artifact-tool')).href);
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load('Output/outputs/2026-10-20-stocktake/UK Central Wholesale - Stocktake Template.xlsx'));
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:1000})).ndjson);
console.log((await wb.inspect({kind:'table',range:'Stocktake!A1:H3',include:'values',tableMaxRows:3,tableMaxCols:8,maxChars:1800})).ndjson);

