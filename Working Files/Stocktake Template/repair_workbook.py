from pathlib import Path
import io
import zipfile
import xml.etree.ElementTree as ET

p = Path('Output/outputs/2026-10-20-stocktake/UK Central Wholesale - Stocktake Template.xlsx')
ns = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
mc = 'http://schemas.openxmlformats.org/markup-compatibility/2006'
ET.register_namespace('', ns)
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
with zipfile.ZipFile(p) as z:
    entries = z.infolist()
    original = {e.filename:z.read(e.filename) for e in entries}
root = ET.fromstring(original['xl/workbook.xml'])
# Removing the instructions with ElementTree dropped namespace declarations used
# only by compatibility attribute values. Remove optional Excel UI/revision
# metadata and the now-invalid compatibility declaration; retain all data parts.
root.attrib.pop(f'{{{mc}}}Ignorable', None)
for child in list(root):
    if child.tag == f'{{{mc}}}AlternateContent' or child.tag.endswith('}revisionPtr'):
        root.remove(child)
for item in root.iter():
    for key in list(item.attrib):
        if key.startswith('{http://schemas.microsoft.com/'):
            del item.attrib[key]
repaired = ET.tostring(root, encoding='utf-8', xml_declaration=True)
updates = {'xl/workbook.xml': repaired}
for name, namespace in [('[Content_Types].xml','http://schemas.openxmlformats.org/package/2006/content-types'),('xl/_rels/workbook.xml.rels','http://schemas.openxmlformats.org/package/2006/relationships')]:
    ET.register_namespace('',namespace)
    updates[name]=ET.tostring(ET.fromstring(original[name]),encoding='utf-8',xml_declaration=True)
buffer = io.BytesIO()
with zipfile.ZipFile(buffer,'w') as z:
    for entry in entries:
        z.writestr(entry,updates.get(entry.filename,original[entry.filename]))
with zipfile.ZipFile(buffer) as z:
    assert z.testzip() is None
    for entry in entries:
        if entry.filename not in updates:
            assert z.read(entry.filename) == original[entry.filename]
    for name in z.namelist():
        if not name.endswith(('.xml','.rels')):
            continue
        data=z.read(name)
        declarations={prefix for _,(prefix,uri) in ET.iterparse(io.BytesIO(data),events=['start-ns'])}
        for element in ET.fromstring(data).iter():
            for attr,value in element.attrib.items():
                if attr == f'{{{mc}}}Ignorable' or attr == 'Requires':
                    assert all(prefix in declarations for prefix in value.split()), (name,attr,value)
    assert [s.get('name') for s in ET.fromstring(z.read('xl/workbook.xml')).find(f'{{{ns}}}sheets')] == ['Stocktake']
p.write_bytes(buffer.getvalue())
print('Repaired workbook metadata. All other parts are unchanged. XML and compatibility namespace checks passed.')
