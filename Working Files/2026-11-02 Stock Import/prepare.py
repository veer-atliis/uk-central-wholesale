import collections
import hashlib
import json
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Go Live Files/Edited/UK_Central_Wholesale_Stocktake_with_Last_Cost.xlsx'
workbook = openpyxl.load_workbook(SOURCE, read_only=True, data_only=True)
import_rows = [list(r) for r in list(workbook['Stocktake (IMPORT)'].values)[1:] if r[0]]
quantity_source = ROOT / 'Go Live Files/Client Supplied/UK_Central_Wholesale_-_Stocktake_1_Oct_2026.xlsx'
quantity_workbook = openpyxl.load_workbook(quantity_source, read_only=True, data_only=True)
stocktake_rows = [list(r) for r in list(quantity_workbook['Stocktake'].values)[1:] if r[0]]
products = collections.defaultdict(list)
for row_number, row in enumerate(list(workbook['Product ID & Cost'].values)[1:], 2):
    if row[0] is not None:
        products[str(row[0])].append({'name': row[1], 'templateId': str(row[3]), 'sourceRow': row_number})

# Preserve the historical full export; supplement it with the supplied new-product export.
product_update_source = ROOT / 'Go Live Files/Client Supplied/Product (product.template) (2).xlsx'
product_update_workbook = openpyxl.load_workbook(product_update_source, read_only=True, data_only=True)
product_updates = []
for row_number, row in enumerate(list(product_update_workbook['Sheet1'].values)[1:], 2):
    if row[0] is not None:
        update = {'code':str(row[0]), 'name':row[1], 'externalId':row[2], 'templateId':str(row[3]),
                  'cost':row[4], 'sourceRow':row_number, 'sourceFile':str(product_update_source), 'suppliedDate':'2026-11-02'}
        assert update['code']=='1023966' and update['templateId']=='2446'
        assert update['externalId']=='__export__.product_template_2446_c565a8f6'
        assert update['cost']==118.42
        assert not products[update['code']], 'Unexpected existing Galaxy mapping; investigate before replacing'
        products[update['code']].append(update)
        product_updates.append(update)
assert len(product_updates)==1

problem_codes = {str(r[0]) for r in stocktake_rows if len(products[str(r[0])]) > 1}
issues = {
    'BDT80': 'Duplicate reference restored on both Odoo products, as confirmed on 2 November 2026. Names differ by NEW. Confirm which product should receive the source count of 55, or whether it must be split between the records.',
    'BFH130': 'Duplicate reference: Barratt Flump Hearts 12x130g versus the same name ending NEW PRODUCT. This line is in the authoritative original stocktake but absent from the last-cost workbook. Confirm the intended product record.',
    'BFS120': 'Duplicate reference: Fruity Mix versus Squishy Sunburst. Stocktake description says Squishy; existing lookup selects Fruity Mix (868). Confirm the actual counted product.',
    'BT03': 'Duplicate reference: standard versus NEW PRODUCT. Confirm which product received the count and check the source fractional quantity of 20.33.',
    'CM05': 'Duplicate reference and pack-size mismatch: stocktake description says 48x49g; existing lookup selects 48x54g (1861). Confirm actual pack size.',
    'CO07S': 'Two exported products have the same reference and name. Confirm the intended product record and give each product a unique reference.',
    'EC03': 'Two exported products have the same reference and name. Confirm the intended product record and give each product a unique reference.',
    'GC01': 'Duplicate reference and pack-size mismatch: stocktake description says 48x54g; existing lookup selects 48x49g (1211). Confirm actual pack size.',
    'LFG130': 'Duplicate reference: product names differ by BAG. Confirm which product received the count and the unit being counted.',
    'LLG130': 'Duplicate reference: product names differ by BAG. Confirm which product received the count and the unit being counted.',
    'LMG130': 'Duplicate reference: Midget Gems BAG versus Mini Gems. Confirm the actual counted product.',
}
ready = []
review = []
excluded = []
previous_lookup = {str(r[0]): str(r[5]) for r in import_rows}
for excel_row, row in enumerate(stocktake_rows, 2):
    code = str(row[0])
    if code == 'MISC':
        excluded.append({'code':code,'description':row[1],'unit':row[2],'quantity':row[3],
                         'reason':"Exclude from import: Nitin's decision confirmed by Veer on 2 November 2026. Original source quantity retained for reconciliation."})
    elif code in problem_codes:
        issue = issues[code]
        if row[4]:
            issue += '\nSource note: ' + str(row[4])
        review.append({'code': code, 'description': row[1], 'unit': row[2], 'quantity': row[3],
                       'issue': issue, 'candidates': products[code], 'selectedTemplateId': previous_lookup.get(code),
                       'sourceSheet': 'Stocktake', 'sourceRow': excel_row})
    else:
        assert len(products[code]) == 1, f'Unresolved reference: {code}'
        ready.append(row[:5])

assert len(ready) == 467 and len(review) == 11 and len(excluded) == 1
assert {r['code'] for r in review} == problem_codes
assert len({r[0] for r in ready}) == len(ready)
assert not ({r[0] for r in ready} & {r['code'] for r in review})
assert {r[0] for r in ready} | {r['code'] for r in review} | {r['code'] for r in excluded} == {r[0] for r in stocktake_rows}
assert all(isinstance(r[3], (int, float)) for r in ready)
data = {'source': str(quantity_source), 'sourceSha256': hashlib.sha256(quantity_source.read_bytes()).hexdigest(),
        'lookupSource': str(SOURCE), 'lookupSourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'productUpdates':product_updates, 'productUpdateSourceSha256':hashlib.sha256(product_update_source.read_bytes()).hexdigest(),
        'ready': ready, 'review': review, 'excluded': excluded,
        'sourceCount': len(stocktake_rows), 'importSourceCount': len(import_rows),
        'readyQuantity': sum(r[3] for r in ready), 'reviewQuantity': sum(r['quantity'] for r in review),
        'excludedQuantity':sum(r['quantity'] for r in excluded),
        'totalQuantity': sum(r[3] for r in stocktake_rows),
        'unitStatus':'All source Unit of Measure cells are blank. Veer does not know the counted unit; preserve the numeric counts without conversion. Odoo interprets them in the configured inventory unit.',
        'galaxyEvidence':'Product 1023966, **GALAXY BLOCK 17X360G; supplied screenshot confirms Units and inventory tracking. Supplied product.template export confirms template ID 2446, External ID __export__.product_template_2446_c565a8f6, and cost 118.42. No variant or inventory-record ID supplied.'}
assert abs(data['readyQuantity'] + data['reviewQuantity'] + data['excludedQuantity'] - data['totalQuantity']) < 1e-8
(Path(__file__).parent / 'data.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in data.items() if k not in {'ready', 'review', 'excluded'}}, indent=2))
