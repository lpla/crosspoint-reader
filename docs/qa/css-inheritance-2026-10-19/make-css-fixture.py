from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

out = Path(__file__).resolve().parent / 'fixtures'
out.mkdir(exist_ok=True)
css = 'body{font-family:serif}p{margin:0 0 1em 0;text-indent:0}.parent{font-weight:bold;font-style:italic}.inherit{font-weight:normal;font-style:normal}#child{font-weight:inherit;font-style:inherit}'
short = '<p class="parent">Matched emphasis</p><div class="parent"><p id="child" class="inherit">Matched emphasis</p></div><p>Matched regular</p><div class="parent"><p style="font-weight:normal;font-style:normal"><span style="font-weight:inherit;font-style:inherit">Matched regular</span></p></div><p>End of inheritance check.</p>'
long = ''.join('<div class="parent"><p id="r' + str(i) + '" style="font-weight:inherit;font-style:inherit">Paragraph ' + str(i) + '. Original test text for partial layout, inheritance and resume. The parent emphasis must survive the CSS reset without leaking into the following paragraph.</p></div><p>Regular sibling text.</p>' for i in range(1200))
with ZipFile(out / 'css-inheritance.epub', 'w') as z:
    z.writestr('mimetype', 'application/epub+zip')
    z.writestr('META-INF/container.xml', '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0"><rootfiles><rootfile full-path="content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
    z.writestr('style.css', css, compress_type=ZIP_DEFLATED)
    for i, body in enumerate((short, long)):
        z.writestr(f'case{i}.xhtml', '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Original inheritance fixture</title><link rel="stylesheet" href="style.css"/></head><body>' + body + '</body></html>', compress_type=ZIP_DEFLATED)
    z.writestr('content.opf', '<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="uid"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>CSS inheritance QA</dc:title><dc:creator>CrossPoint QA</dc:creator><dc:identifier id="uid">qa-20261019-inherit</dc:identifier><dc:language>en</dc:language></metadata><manifest><item id="css" href="style.css" media-type="text/css"/><item id="c0" href="case0.xhtml" media-type="application/xhtml+xml"/><item id="c1" href="case1.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="c0"/><itemref idref="c1"/></spine></package>')
print(out / 'css-inheritance.epub')
