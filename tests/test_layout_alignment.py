from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
ROOT = Path(__file__).resolve().parents[1]


def paragraphs(docx_path):
    with ZipFile(docx_path) as zf:
        xml = zf.read('word/document.xml')
    root = ET.fromstring(xml)
    out = []
    for p in root.findall('.//w:body/w:p', NS):
        text = ''.join(t.text or '' for t in p.findall('.//w:t', NS))
        jc = p.find('./w:pPr/w:jc', NS)
        val = jc.attrib.get('{%s}val' % NS['w']) if jc is not None else None
        out.append((text, val))
    return out


def test_main_title_author_are_not_justified():
    pars = paragraphs(ROOT / 'manuscript' / 'MSBP_Tg_Journal_Manuscript.docx')
    display = pars[:4]
    assert display[0][0].startswith('Mobility Suppression Boundary Principle')
    assert display[1][0].startswith('A within-fiber')
    assert display[2][0].startswith('Htet Ko Ko Naing')
    assert display[3][0].startswith('Preprint manuscript')
    assert [val for _, val in display] == ['left', 'left', 'left', 'center']


def test_supplement_title_author_are_not_justified():
    pars = paragraphs(ROOT / 'supplementary' / 'Supplementary_Methods.docx')
    display = pars[:3]
    assert display[0][0].startswith('Supplementary Methods')
    assert display[1][0].startswith('Mobility Suppression Boundary Principle')
    assert display[2][0].startswith('Author: Htet Ko Ko Naing')
    assert [val for _, val in display] == ['left', 'left', 'left']


def test_supplement_manual_numbered_lists_are_plain_not_bulleted():
    with ZipFile(ROOT / 'supplementary' / 'Supplementary_Methods.docx') as zf:
        xml = zf.read('word/document.xml')
    root = ET.fromstring(xml)
    for p in root.findall('.//w:body/w:p', NS):
        text = ''.join(t.text or '' for t in p.findall('.//w:t', NS)).strip()
        if text[:2] in {'1.', '2.', '3.', '4.', '5.', '6.', '7.'}:
            pstyle = p.find('./w:pPr/w:pStyle', NS)
            style_val = pstyle.attrib.get('{%s}val' % NS['w']) if pstyle is not None else ''
            assert 'Bullet' not in style_val
