"""Remove an authorised tab using OOXML because Artifact Tool exposes no documented sheet deletion API.
Cell values/layout are authored by Artifact Tool; openpyxl is used for read-only QA.
"""
from pathlib import Path, PurePosixPath
import json, zipfile, posixpath, shutil, hashlib
import xml.etree.ElementTree as ET
from decimal import Decimal
import openpyxl

work=Path(__file__).resolve().parent
root=work.parents[1]
stage=work/'workflow-stage.xlsx'
final=work/'workflow-checked.xlsx'
ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
rel_ns='http://schemas.openxmlformats.org/package/2006/relationships'
ct_ns='http://schemas.openxmlformats.org/package/2006/content-types'
def xml_bytes(element,default_ns):
    ET.register_namespace('',default_ns)
    ET.register_namespace('r',ns['r'])
    ET.register_namespace('vt','http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes')
    return ET.tostring(element,encoding='utf-8',xml_declaration=True)
def relative(owner,target):
    return target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join(posixpath.dirname(owner),target))
with zipfile.ZipFile(stage) as z:
    parts={n:z.read(n) for n in z.namelist()}
book=ET.fromstring(parts['xl/workbook.xml'])
rels=ET.fromstring(parts['xl/_rels/workbook.xml.rels'])
sheets=book.find('s:sheets',ns)
remove_sheet=next(s for s in sheets if s.attrib['name']=='Product matches')
removed_index=list(sheets).index(remove_sheet)
rid=remove_sheet.attrib['{'+ns['r']+'}id']
rel=next(r for r in rels if r.attrib['Id']==rid)
sheetpart=relative('xl/workbook.xml',rel.attrib['Target'])
removed={sheetpart}
sheetrels=posixpath.join(posixpath.dirname(sheetpart),'_rels',posixpath.basename(sheetpart)+'.rels')
if sheetrels in parts:
    removed.add(sheetrels)
    for item in ET.fromstring(parts[sheetrels]):
        if item.attrib.get('TargetMode')!='External': removed.add(relative(sheetpart,item.attrib['Target']))
sheets.remove(remove_sheet)
rels.remove(rel)
names=book.find('s:definedNames',ns)
if names is not None:
    for item in list(names):
        if 'localSheetId' in item.attrib:
            index=int(item.attrib['localSheetId'])
            if index==removed_index: names.remove(item)
            elif index>removed_index: item.set('localSheetId',str(index-1))
client_sheet=next(s for s in sheets if s.attrib['name']=='Client review')
client_rel=next(r for r in rels if r.attrib['Id']==client_sheet.attrib['{'+ns['r']+'}id'])
clientpart=relative('xl/workbook.xml',client_rel.attrib['Target'])
client_xml=ET.fromstring(parts[clientpart])
# The quantity response moved from H to F. Remove only obsolete H validation if retained by clear(all).
validations=client_xml.find('s:dataValidations',ns)
if validations is not None:
    for item in list(validations):
        if item.attrib.get('sqref')=='H2:H12': validations.remove(item)
    validations.set('count',str(len(validations)))
    if not len(validations): client_xml.remove(validations)
parts[clientpart]=xml_bytes(client_xml,ns['s'])
types=ET.fromstring(parts['[Content_Types].xml'])
for item in list(types):
    if item.attrib.get('PartName','').lstrip('/') in removed: types.remove(item)
parts['xl/workbook.xml']=xml_bytes(book,ns['s'])
parts['xl/_rels/workbook.xml.rels']=xml_bytes(rels,rel_ns)
parts['[Content_Types].xml']=xml_bytes(types,ct_ns)
if 'docProps/app.xml' in parts:
    app=ET.fromstring(parts['docProps/app.xml'])
    ap={'a':'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties','v':'http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes'}
    titles=app.find('a:TitlesOfParts/v:vector',ap)
    if titles is not None:
        for child in list(titles):
            if child.text=='Product matches': titles.remove(child)
        titles.set('size',str(len(titles)))
    heading=app.find('a:HeadingPairs/v:vector',ap)
    if heading is not None:
        variants=list(heading)
        for i in range(len(variants)-1):
            if any(c.text=='Worksheets' for c in variants[i]):
                for c in variants[i+1]:
                    if c.tag.endswith('i4'): c.text=str(len(sheets))
    parts['docProps/app.xml']=xml_bytes(app,ap['a'])
with zipfile.ZipFile(final,'w',zipfile.ZIP_DEFLATED) as z:
    for n,data in parts.items():
        if n not in removed: z.writestr(n,data)

before=json.loads((work/'workflow-before.json').read_text())
check=openpyxl.load_workbook(final,read_only=False,data_only=False)
assert check.sheetnames==['Client review','Excluded']
client=check['Client review']
assert [c.value for c in client[1]][:7]==['Current internal reference','Product on stocktake','Stocktake quantity','What to check','Final internal reference','Quantity to import','Notes / changes needed']
for i,row in enumerate(before['rows'],2):
    assert [client.cell(i,c).value for c in [1,2,3,4]]==[row[0],row[1],row[3],row[4]]
    assert client.cell(i,5).value==row[6]
    assert client.cell(i,6).value==row[7]
    notes='\n'.join(str(x) for x in [row[5],None if row[2] is None else 'Counted as: '+str(row[2])] if x is not None and x!='') or None
    assert client.cell(i,7).value==notes
assert [[c.value for c in row] for row in check['Excluded'].iter_rows(min_row=1,max_row=2,max_col=5)]==before['excluded']
assert sum(Decimal(str(client.cell(r,3).value)) for r in range(2,13))==Decimal('293.33')
assert check['Excluded']['D2'].value==15
assert client.freeze_panes=='A2'
assert client.tables['ClientreviewTable'].ref=='A1:G12'
assert [c.name for c in client.tables['ClientreviewTable'].tableColumns]==[c.value for c in client[1]][:7]
assert {str(v.sqref) for v in client.data_validations.dataValidation}=={'F2:F12'}
assert all(client.cell(r,8).value is None for r in range(1,18))
assert not any(c.data_type in ('f','e') for s in check for row in s for c in row)
assert 'Product matches' not in str([row for s in check for row in s.values])
check.close()
target=root/'Go Live Files/Edited/Stock Import/Stock Import - Client Review.xlsx'
try: shutil.copyfile(final,target)
except PermissionError:
    target=root/'Output/outputs/2026-11-03-stock-review/Stock Import - Client Review.xlsx'
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(final,target)
assert hashlib.sha256(target.read_bytes()).digest()==hashlib.sha256(final.read_bytes()).digest()
result={'path':str(target),'sheets':['Client review','Excluded'],'review_lines':11,'review_total':'293.33','excluded_quantity':15,'responses_preserved':True,'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
(work/'workflow-validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
