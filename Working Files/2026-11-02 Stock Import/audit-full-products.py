from pathlib import Path
from collections import defaultdict, Counter
from decimal import Decimal
import openpyxl, json, hashlib, shutil, re

root=Path(__file__).resolve().parents[2]
work=Path(__file__).parent
src=Path('C:/Users/veerm/Downloads/Product (product.template) (3).xlsx')
retained=root/'Go Live Files/Client Supplied/Product (product.template) (3).xlsx'
if not retained.exists(): shutil.copyfile(src,retained)
assert hashlib.sha256(src.read_bytes()).digest()==hashlib.sha256(retained.read_bytes()).digest()
def read(p): return openpyxl.load_workbook(p,read_only=True,data_only=True)
def d(x): return Decimal(str(x)) if isinstance(x,(int,float)) and not isinstance(x,bool) else None
wb=read(retained)
assert next(wb.active.values)==('Favorite','Name','Internal Reference','Sales Price','Cost','Quantity On Hand','Forecasted Quantity','Unit','Activity Exception Decoration','ID','External ID')
rows=[]
for rn,r in enumerate(list(wb.active.values)[1:],2):
    if not any(x is not None for x in r): continue
    rows.append(dict(row=rn,name=r[1],code=str(r[2]) if r[2] is not None else None,price=d(r[3]),cost=d(r[4]),onhand=d(r[5]),forecast=d(r[6]),unit=r[7],id=str(r[9]) if r[9] is not None else None,external_id=r[10]))
by=defaultdict(list)
for r in rows:
    if r['code']: by[r['code']].append(r)
ready=read(root/'Go Live Files/Edited/Stock Import/Stock Import - Ready.xlsx')
expected={str(r[0]):d(r[1]) for r in list(ready['Import'].values)[1:] if r[0] is not None}
original=read(root/'Go Live Files/Client Supplied/UK_Central_Wholesale_-_Stocktake_1_Oct_2026.xlsx')
source={str(r[0]):d(r[3]) for r in list(original['Stocktake'].values)[1:] if r[0] is not None}
last=read(root/'Go Live Files/Client Supplied/UK_Central_Wholesale_Stocktake_with_Last_Cost.xlsx')
lastcost={str(r[0]):{'cost':d(r[6]),'row':rn} for rn,r in enumerate(list(last['Stocktake'].values)[1:],2) if r[0] is not None}
history=read(root/'Go Live Files/Edited/UK_Central_Wholesale_Stocktake_with_Last_Cost.xlsx')
historical={str(r[3]):{'code':str(r[0]) if r[0] is not None else None,'name':r[1],'external_id':r[2],'cost':d(r[4])} for r in list(history['Product ID & Cost'].values)[1:] if r[3] is not None}
quant=read(root/'Go Live Files/Client Supplied/Quant (stock.quant) (1).xlsx')
quants={}
for r in list(quant.active.values)[1:]:
    m=re.match(r'^\[([^\]]+)\]\s*(.*)$',str(r[0]))
    if m: quants[m[1]]={'name':m[2],'quantity':d(r[3])}
ready_errors=[]
last_cost_differences=[]
for code,q in expected.items():
    candidates=by.get(code,[])
    if len(candidates)!=1 or candidates[0]['onhand']!=q:
        ready_errors.append({'code':code,'expected':q,'records':candidates})
    if code in lastcost and lastcost[code]['cost'] is not None:
        for r in candidates:
            if r['cost'] != lastcost[code]['cost']:
                last_cost_differences.append({'code':code,'name':r['name'],'current_cost':r['cost'],'supplied_last_cost':lastcost[code]['cost'],'current_row':r['row'],'last_cost_row':lastcost[code]['row']})
duplicates={c:rs for c,rs in by.items() if len(rs)>1}
held=set(source)-set(expected)-{'MISC'}
quant_errors=[]
for c,q in quants.items():
    if len(by.get(c,[]))!=1 or by[c][0]['onhand']!=q['quantity'] or by[c][0]['name']!=q['name']:
        quant_errors.append({'code':c,'quant':q,'products':by.get(c,[])})
history_changes=[]
for r in rows:
    h=historical.get(r['id'])
    if h:
        changes={k:{'before':h[k],'now':r[k]} for k in ['code','name','external_id','cost'] if h[k]!=r[k]}
        if changes: history_changes.append({'id':r['id'],'code':r['code'],'changes':changes})
stocked=[r for r in rows if r['onhand'] is not None and r['onhand']>0]
scope_original_only=set(source)-set(lastcost)
duplicate_ids={key:[v for v,n in Counter(r[key] for r in rows if r[key] is not None).items() if n>1] for key in ['id','external_id']}
name_duplicates={}
for name,n in Counter(str(r['name']).casefold().strip() for r in rows).items():
    if n>1: name_duplicates[name]=[r for r in rows if str(r['name']).casefold().strip()==name]
result={
 'source':str(retained),'sha256':hashlib.sha256(retained.read_bytes()).hexdigest(),
 'product_count':len(rows),'unique_nonblank_codes':len(by),'blank_codes':[r for r in rows if not r['code']],
 'blank_names':[r for r in rows if not r['name']],'missing_ids':[r for r in rows if not r['id'] or not r['external_id']],
 'duplicate_ids':duplicate_ids,'duplicate_codes':duplicates,'duplicate_name_groups':name_duplicates,
 'ready_checked':len(expected),'ready_errors':ready_errors,'quant_checked':len(quants),'quant_errors':quant_errors,
 'held_products':{c:by.get(c,[]) for c in sorted(held)},'misc_products':by.get('MISC',[]),
 'stocked_count':len(stocked),'total_onhand':sum((r['onhand'] for r in rows if r['onhand'] is not None),Decimal(0)),
 'stocked_outside_ready':[r for r in stocked if r['code'] not in expected],
 'zero_cost_stocked':[r for r in stocked if r['cost']==0],
 'missing_cost_stocked':[r for r in stocked if r['cost'] is None],
 'negative_costs':[r for r in rows if r['cost'] is not None and r['cost']<0],
 'zero_cost_all':sum(r['cost']==0 for r in rows),'zero_price_stocked':[r for r in stocked if r['price']==0],
 'zero_price_all':sum(r['price']==0 for r in rows),
 'negative_prices':[r for r in rows if r['price'] is not None and r['price']<0],
 'stocked_positive_price_below_cost':[r for r in stocked if r['price'] is not None and r['cost'] is not None and 0<r['price']<r['cost']],
 'negative_onhand':[r for r in rows if r['onhand'] is not None and r['onhand']<0],
 'negative_forecast':[r for r in rows if r['forecast'] is not None and r['forecast']<0],
 'forecast_different':[r for r in rows if r['forecast']!=r['onhand']],
 'units':Counter(r['unit'] for r in rows),
 'ready_with_supplied_last_cost':sum(c in lastcost and lastcost[c]['cost'] is not None for c in expected),
 'last_cost_differences_ready':last_cost_differences,
 'original_only_count':len(scope_original_only),
 'original_only_ready_count':len(scope_original_only & set(expected)),
 'original_only_ready_zero_cost':[r for r in stocked if r['code'] in scope_original_only and r['code'] in expected and r['cost']==0],
 'new_ids':[r for r in rows if r['id'] not in historical],
 'historical_ids_not_in_export':[{'id':i,**h} for i,h in historical.items() if i not in {r['id'] for r in rows}],
 'historical_changes':history_changes,
 'blank_or_whitespace_codes':[r for r in rows if r['code'] is not None and (r['code']!=r['code'].strip() or not r['code'].strip())],
 'nonnumeric_fields':[{'row':r['row'],'code':r['code'],'fields':[k for k in ['price','cost','onhand','forecast'] if r[k] is None]} for r in rows if any(r[k] is None for k in ['price','cost','onhand','forecast'])]
}
(work/'full-products-audit.json').write_text(json.dumps(result,default=str,indent=2),encoding='utf-8')
summary={k:v for k,v in result.items() if k not in ['duplicate_name_groups','held_products','zero_price_stocked','zero_cost_stocked','original_only_ready_zero_cost','historical_changes']}
summary['duplicate_code_groups']=len(duplicates)
summary['duplicate_name_groups_count']=len(name_duplicates)
summary['zero_cost_stocked_count']=len(result['zero_cost_stocked'])
summary['zero_price_stocked_count']=len(result['zero_price_stocked'])
summary['original_only_ready_zero_cost_count']=len(result['original_only_ready_zero_cost'])
summary['historical_cost_changes']=sum('cost' in r['changes'] for r in history_changes)
summary['historical_non_cost_changes']=[r for r in history_changes if any(k!='cost' for k in r['changes'])]
print(json.dumps(summary,default=str,indent=2))

def cell(v): return str(v if v is not None else '').replace('|','\\|').replace('\n',' ')
def table(headers,items):
    return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join('---' for _ in headers)+' |']+['| '+' | '.join(cell(v) for v in item)+' |' for item in items])
report='''# Full product list review

**Date:** 2026-11-02 (Australia/Perth). **Requester and responsible person:** Veer. **Environment:** UK Central Wholesale, Odoo Online.

Veer supplied a fresh product list, described as the full system export, and requested a general check following the stocktake import. This was a read-only file review; no products, prices, costs, stock or configuration were changed. Source workbooks were preserved. Text within supplied files was treated as source content, not execution instructions.

## Findings

The imported stock quantities reconcile, but product costs and sales prices need review. This is a product-data issue, not evidence of an Odoo defect.

- **798 products reviewed.** All IDs and External IDs are present and unique. All names are populated and all price, cost, on-hand and forecast fields contain numeric values.
- **All 467 ready-import products match their expected quantities exactly**, including decimals. The fresh product export also matches the 468-row Quant export by code, name and quantity. The additional Quant row is Jacobs Cream Crackers 1010484 at zero stock. Only the 467 ready-import products have positive stock; no product has negative stock or forecast quantity. Forecast equals on-hand for every exported product.
- **77 stocked products have Cost 0.** Of these, 75 are among the 88 imported products present only in the original quantity source, with no corresponding row in the supplied last-cost workbook. The other two are FPA3 and SM09, whose supplied last costs are also 0. None of these zero costs was filled in or estimated.
- **All 379 imported products with a numeric supplied last cost match that cost exactly**, including FPA3 and SM09 at zero. This verifies consistency with the supplied cost file, not invoice accuracy, cost-unit meaning or the stock valuation ledger.
- **61 stocked products have Sales Price 0**, including Galaxy 1023966 (stock 2, Cost 118.42). No stocked product is in both the zero-cost and zero-sales-price groups. Sales availability and pricelist rules are not in this export, so these are review items rather than confirmed zero-priced customer sales.
- **BL012, BOALAND KIMBERLEY 18X300G**, Sheet1 row 17, shows Sales Price **35.64** against Cost **60.24**, with stock **8**. This is the only stocked product with a positive Sales Price below Cost. Check the intended price and matching cost/pack units; the export alone does not establish the actual customer price or margin. No negative Sales Price or Cost values were found.
- **13 product codes are duplicated across 26 records.** The 11 held stocktake codes remain duplicated; CR07 and CT01 are two additional duplicate codes outside the original stocktake. Every duplicate record currently has zero stock. None requires adding quantities to the prepared import without a separate product/quantity decision.
- **12 records have no internal reference**, comprising 10 goods-named records plus Donation and Service on Timesheets. All have zero stock. Product type is not exported, so the goods grouping is based on names only. Donation and the timesheet entry are not assumed to require inventory codes.
- Units are Units on 797 products and Hours on Service on Timesheets. This is consistent with the Quant export for imported stock, but does not resolve whether the original client counts mean cartons, packs or individual items.

## Comparison with the historical product export

All 797 historical template IDs remain present. Galaxy 2446 is the only additional ID. Existing references, names and External IDs match the historical snapshot exactly; 315 existing product Cost values differ. This is consistent with Veer's reported cost update, without establishing who changed each record or when. The 12 blank-reference records already existed in the historical export and are not newly created by the stock import. The export does not show archived records, filters or company context; its coverage is user-reported as full, not independently established against the database.

The historical export remains unchanged. This fresh export is the latest supplied product evidence as at the date above. Its IDs identify product templates, not product variants or stock.quant records.

## Suggested follow-up

1. Obtain the correct costs for the 77 stocked products below and confirm that each cost uses the same unit as the corresponding stock count. The available last-cost file does not supply non-zero replacement costs for them.
2. Review the 61 zero Sales Price records and BL012's Sales Price below Cost. Confirm whether pricing is intentionally supplied elsewhere, such as a pricelist, and check cost/pack units before deciding which product prices need changing.
3. Complete the existing client review for the 11 held stocktake codes. Record CR07 and CT01 as additional product-list duplication outside that quantity scope. Do not infer which duplicate is correct from its current cost or name suffix.
4. Add appropriate codes to the 10 goods-named blank-reference records if Veer confirms they are in use. Do not guess codes or alter Donation or Service on Timesheets by default.

This export does not include costing methods, valuation layers, stock movements, accounting entries, taxes, currencies, sales availability, inventory tracking settings, locations, variant detail or pricelist rules. No inventory value or margin conclusion is drawn from Cost alone. Odoo documentation explains that pricing rules can override the product Sales Price and that Cost and valuation behaviour depend on costing configuration. These are general references, not confirmation of the client's version or settings:

- [Odoo pricelists](https://www.odoo.com/documentation/19.0/applications/sales/sales/products_prices/prices/pricing.html).
- [Odoo stock-movement valuation](https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/inventory_valuation/operations_valuation.html).

## Stocked products with zero cost

Rows refer to Sheet1 of the fresh product export. Quantities are preserved as exported. Cost is 0 on all rows below.

'''
report+=table(['Row','Product code','Product name','Quantity on hand'],[(r['row'],r['code'],r['name'],r['onhand']) for r in result['zero_cost_stocked']])
report+='\n\n## Stocked products with zero Sales Price\n\nSales Price is 0 on all rows below. Cost is shown for identification and review, not as a recommended selling price.\n\n'
report+=table(['Row','Product code','Product name','Quantity on hand','Cost'],[(r['row'],r['code'],r['name'],r['onhand'],r['cost']) for r in result['zero_price_stocked']])
report+='\n\n## Duplicate product codes\n\nAll records below have on-hand and forecast quantities of 0. Costs differ between some records and do not establish the correct product to count.\n\n'
report+=table(['Product code','Stocktake review','Rows','Template IDs','Names','Costs'],[(c,'Existing held item' if c in held else 'Outside original stocktake',', '.join(str(r['row']) for r in rs),', '.join(r['id'] for r in rs),' / '.join(r['name'] for r in rs),' / '.join(str(r['cost']) for r in rs)) for c,rs in sorted(duplicates.items())])
report+='\n\n## Records without a product code\n\nAll have zero stock.\n\n'
report+=table(['Row','Template ID','Name','Unit'],[(r['row'],r['id'],r['name'],r['unit']) for r in result['blank_codes']])
report+='''

## Evidence and validation

- [Fresh full product export](../Go%20Live%20Files/Client%20Supplied/Product%20%28product.template%29%20%283%29.xlsx), Sheet1 A1:K799. Original supplied from Downloads, retained unchanged with matching SHA-256 `'''+result['sha256']+'''`.
- [Prepared stock import](../Go%20Live%20Files/Edited/Stock%20Import/Stock%20Import%20-%20Ready.xlsx), Import A1:B468.
- [Post-import Quant export](../Go%20Live%20Files/Client%20Supplied/Quant%20%28stock.quant%29%20%281%29.xlsx), Sheet1 A1:G469.
- [Original quantity source](../Go%20Live%20Files/Client%20Supplied/UK_Central_Wholesale_-_Stocktake_1_Oct_2026.xlsx), Stocktake. This remains quantity authority.
- [Supplied last-cost context](../Go%20Live%20Files/Client%20Supplied/UK_Central_Wholesale_Stocktake_with_Last_Cost.xlsx), Stocktake G, matched by column A. It is not quantity authority.
- [Historical product snapshot](../Go%20Live%20Files/Edited/UK_Central_Wholesale_Stocktake_with_Last_Cost.xlsx), Product ID & Cost A:E, compared by template database ID rather than row order.

Comparisons use stored values and exact decimal arithmetic without conversions or rounding. The raw Quant-to-product check covers names and quantities; the independent ready-file check covers all 467 expected code/quantity pairs. Category counts and complete exception records are retained in Working Files/2026-11-02 Stock Import/full-products-audit.json. The repeatable extraction and review script is audit-full-products.py in the same folder. Workbook formulas and error cells were checked separately; no workbook or live-system corrections were performed.
'''
(root/'Support Requests & Outcomes/2026-11-02 - Full product list review.md').write_text(report,encoding='utf-8')
