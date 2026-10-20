from pathlib import Path, PurePosixPath
import io
import zipfile
import xml.etree.ElementTree as ET

target = Path('Output/outputs/2026-10-20-stocktake/UK Central Wholesale - Stocktake Template.xlsx')
main = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
rel = 'http://schemas.openxmlformats.org/package/2006/relationships'
docrel = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
ET.register_namespace('', main)
ET.register_namespace('r', docrel)
with zipfile.ZipFile(target) as archive:
    original = {entry.filename: archive.read(entry.filename) for entry in archive.infolist()}
    entries = archive.infolist()
book = ET.fromstring(original['xl/workbook.xml'])
sheets = book.find(f'{{{main}}}sheets')
sheet = next(s for s in sheets if s.get('name') == 'Instructions')
rid = sheet.get(f'{{{docrel}}}id')
sheets.remove(sheet)
relationships = ET.fromstring(original['xl/_rels/workbook.xml.rels'])
relationship = next(r for r in relationships if r.get('Id') == rid)
sheet_path = relationship.get('Target')
sheet_path = sheet_path.lstrip('/') if sheet_path.startswith('/') else str(PurePosixPath('xl') / sheet_path)
relationships.remove(relationship)
types = ET.fromstring(original['[Content_Types].xml'])
for entry in list(types):
    if entry.get('PartName') == '/' + sheet_path:
        types.remove(entry)
updates = {
    'xl/workbook.xml': ET.tostring(book, encoding='utf-8', xml_declaration=True),
    'xl/_rels/workbook.xml.rels': ET.tostring(relationships, encoding='utf-8', xml_declaration=True),
    '[Content_Types].xml': ET.tostring(types, encoding='utf-8', xml_declaration=True),
}
# Direct package editing supplies the worksheet-removal capability absent from
# the documented Artifact Tool API and preserves the remaining sheet byte-for-byte.
buffer = io.BytesIO()
with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
    for entry in entries:
        if entry.filename != sheet_path:
            archive.writestr(entry, updates.get(entry.filename, original[entry.filename]))
with zipfile.ZipFile(buffer) as check:
    assert check.testzip() is None
    saved = ET.fromstring(check.read('xl/workbook.xml'))
    assert [s.get('name') for s in saved.find(f'{{{main}}}sheets')] == ['Stocktake']
    for name, value in original.items():
        if name not in updates and name != sheet_path:
            assert check.read(name) == value, name
target.write_bytes(buffer.getvalue())
print('Removed Instructions. Stocktake sheet, table, formatting and validation are unchanged.')
