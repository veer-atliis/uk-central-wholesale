from pathlib import Path
import json
import zipfile
import xml.etree.ElementTree as ET
import openpyxl

root = Path(__file__).resolve().parents[2]
old_path = root / 'Go Live Files/Edited/Stock Import/Stock Import - Client Review.xlsx'
new_path = root / 'Output/outputs/2026-11-02-stock-review/Stock Import - Client Review.xlsx'
old = openpyxl.load_workbook(old_path, read_only=False, data_only=False)
new = openpyxl.load_workbook(new_path, read_only=False, data_only=False)
assert old.sheetnames == new.sheetnames
def values(book,sheet,ranges):
    return [[book[sheet][cell].value for cell in row] for row in ranges]
for r in range(2,13):
    for col in [1,2,3,4,6,7,8]:
        assert old['Client review'].cell(r,col).value == new['Client review'].cell(r,col).value
for r in range(2,24):
    for col in range(1,4):
        assert old['Product matches'].cell(r,col).value == new['Product matches'].cell(r,col).value
for col in range(1,5):
    assert old['Excluded'].cell(2,col).value == new['Excluded'].cell(2,col).value
for sheet in new:
    assert sheet.freeze_panes == old[sheet.title].freeze_panes
    assert sheet.sheet_view.showGridLines == old[sheet.title].sheet_view.showGridLines
    assert len(sheet.tables) == 1
    table = next(iter(sheet.tables.values()))
    assert [c.name for c in table.tableColumns] == [c.value for c in sheet[1]][:len(table.tableColumns)]
    assert table.autoFilter is not None
    assert not any(c.data_type in ('f','e') for row in sheet for c in row)
assert new['Product matches'].tables['ProductmatchesTable'].ref == 'A1:C23'
assert not any(new['Product matches'].cell(r,c).value is not None for r in range(1,29) for c in [4,5])
assert ET.tostring(new['Client review'].data_validations.to_tree()) == ET.tostring(old['Client review'].data_validations.to_tree())
for sheet in new:
    assert 'Selected in previous lookup' not in str(list(sheet.values))
    assert 'Export Sheet Row' not in str(list(sheet.values))
result = {'review_lines':11,'candidate_products':22,'review_quantity':sum(new['Client review'].cell(r,4).value for r in range(2,13)),'excluded_quantity':new['Excluded']['D2'].value,'checks':'Source values, product identities, blank responses, table headers, filters, frozen headers, validation and absence of formulas/errors verified.'}
(Path(__file__).parent/'simplify-review-validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
