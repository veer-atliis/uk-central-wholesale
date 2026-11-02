from pathlib import Path
from collections import defaultdict, Counter
from decimal import Decimal
import openpyxl
import re, json, hashlib, shutil

root = Path(__file__).resolve().parents[2]
work = Path(__file__).parent
supplied = Path('C:/Users/veerm/Downloads/Quant (stock.quant) (1).xlsx')
retained = root / 'Go Live Files/Client Supplied/Quant (stock.quant) (1).xlsx'
if not retained.exists():
    shutil.copyfile(supplied,retained)
assert hashlib.sha256(supplied.read_bytes()).digest() == hashlib.sha256(retained.read_bytes()).digest()
def read(p):
    return openpyxl.load_workbook(p,read_only=True,data_only=True)
def dec(x):
    return Decimal(str(x)) if isinstance(x,(int,float)) else None
ready = read(root/'Go Live Files/Edited/Stock Import/Stock Import - Ready.xlsx')
imports = [(str(r[0]),dec(r[1])) for r in list(ready['Import'].values)[1:] if r[0] is not None]
source = read(root/'Go Live Files/Client Supplied/UK_Central_Wholesale_-_Stocktake_1_Oct_2026.xlsx')
sources = [(str(r[0]),str(r[1]),dec(r[3])) for r in list(source['Stocktake'].values)[1:] if r[0] is not None]
src = {r[0]:r for r in sources}
review = read(root/'Output/outputs/2026-11-02-stock-review/Stock Import - Client Review.xlsx')
held = {str(r[0]) for r in list(review['Client review'].values)[1:12]}
expected = dict(imports)
export = read(retained)
headers = list(next(export['Sheet1'].values))
assert headers == ['Product','Scheduled','Assigned To','Quantity','Counted','Difference','Unit']
bycode = defaultdict(list)
unparsed = []
for n,r in enumerate(list(export['Sheet1'].values)[1:],2):
    if not any(x is not None for x in r): continue
    match = re.match(r'^\[([^\]]+)\]\s*(.*)$',str(r[0]))
    entry = {'row':n,'product':r[0],'quantity':dec(r[3]),'counted':dec(r[4]),'difference':dec(r[5]),'unit':r[6],'scheduled':str(r[1]),'assigned':r[2]}
    if match:
        entry['code']=match[1]
        entry['name']=match[2]
        bycode[match[1]].append(entry)
    else:
        unparsed.append(entry)
missing = sorted(set(expected)-set(bycode))
extra = {c:rows for c,rows in bycode.items() if c not in expected}
duplicates = {c:rows for c,rows in bycode.items() if len(rows)>1}
mismatches=[]
exact=[]
for code,count in imports:
    if code not in bycode: continue
    total = sum((r['quantity'] for r in bycode[code] if r['quantity'] is not None),Decimal(0))
    if len(bycode[code])==1 and total==count:
        exact.append(code)
    else:
        mismatches.append({'code':code,'expected':count,'export_quantity':total,'rows':bycode[code]})
source_mismatches=[{'code':c,'ready':v,'source':src.get(c)} for c,v in imports if c not in src or v!=src[c][2]]
fractional=[{'code':c,'expected':q,'export':bycode.get(c)} for c,q in imports if q!=q.to_integral_value()]
held_seen={c:bycode[c] for c in sorted(held) if c in bycode}
excluded_seen=bycode.get('MISC',[])
all_rows=[r for rs in bycode.values() for r in rs]+unparsed
result={
 'source_file':str(retained),'source_sha256':hashlib.sha256(retained.read_bytes()).hexdigest(),
 'ready_lines':len(imports),'ready_unique_codes':len(expected),'export_rows':len(all_rows),'export_unique_codes':len(bycode),
 'exact_quantity_matches':len(exact),'ready_total':sum(expected.values(),Decimal(0)),
 'export_quantity_total':sum((r['quantity'] for r in all_rows if r['quantity'] is not None),Decimal(0)),
 'matched_export_total':sum((r['quantity'] for c in expected for r in bycode.get(c,[]) if r['quantity'] is not None),Decimal(0)),
 'missing':missing,'extra':extra,'duplicates':duplicates,'mismatches':mismatches,'source_mismatches':source_mismatches,'fractional':fractional,
 'held_seen':held_seen,'excluded_seen':excluded_seen,'unparsed':unparsed,
 'counted_values':Counter(str(r['counted']) for r in all_rows),'difference_values':Counter(str(r['difference']) for r in all_rows),
 'units':Counter(r['unit'] for r in all_rows),'scheduled':Counter(r['scheduled'] for r in all_rows),
 'zero_expected':[c for c,q in imports if q==0],
 'negative_quantities':[r for r in all_rows if r['quantity'] is not None and r['quantity']<0]
}
(work/'imported-stock-audit.json').write_text(json.dumps(result,default=str,indent=2),encoding='utf-8')
print(json.dumps(result,default=str,indent=2))
