import os, zipfile, xml.etree.ElementTree as ET
path = r"c:\Users\jaikumar\Documents\FitBuddy – AI Fitness Plan Generator using Gemini Models.docx"
print('Path exists:', os.path.exists(path))
if not os.path.exists(path):
    raise SystemExit
with zipfile.ZipFile(path) as z:
    names = z.namelist()
    print('Files:', names[:20])
    xml = z.read('word/document.xml')
    root = ET.fromstring(xml)
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    paras = []
    for p in root.iterfind('.//w:p', ns):
        texts = [t.text or '' for t in p.iterfind('.//w:t', ns)]
        para = ''.join(texts)
        if para.strip():
            paras.append(para)
    text = '\n'.join(paras)
    print('---DOC START---')
    print(text[:10000])
    print('---DOC END---')
