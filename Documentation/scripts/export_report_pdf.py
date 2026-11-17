from pathlib import Path
from io import BytesIO
from xml.sax.saxutils import escape
from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph as WP
from docx.table import Table as WT
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,Image,Table,TableStyle
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import json
R=Path(__file__).resolve().parents[1];doc=Document(R/'AR_Anatomy_Project_Report.docx')
for name,file in [('TimesNewRoman','times.ttf'),('TimesNewRoman-Bold','timesbd.ttf'),('TimesNewRoman-Italic','timesi.ttf'),('TimesNewRoman-BoldItalic','timesbi.ttf'),('Consolas','consola.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('TimesNewRoman',normal='TimesNewRoman',bold='TimesNewRoman-Bold',italic='TimesNewRoman-Italic',boldItalic='TimesNewRoman-BoldItalic')
BASE=ParagraphStyle('Body',fontName='TimesNewRoman',fontSize=11,leading=14,spaceAfter=6,alignment=TA_JUSTIFY)
CENTER=ParagraphStyle('Center',parent=BASE,alignment=TA_CENTER)
H1=ParagraphStyle('H1',parent=BASE,fontName='TimesNewRoman-Bold',fontSize=16,leading=20,textColor=colors.black,spaceBefore=8,spaceAfter=12,keepWithNext=True)
H2=ParagraphStyle('H2',parent=BASE,fontName='TimesNewRoman-Bold',fontSize=12.5,leading=16,textColor=colors.black,spaceBefore=8,spaceAfter=7,keepWithNext=True)
CAP=ParagraphStyle('Caption',parent=CENTER,fontName='TimesNewRoman-Italic',fontSize=9,leading=12,spaceAfter=7)
CELL=ParagraphStyle('Cell',parent=BASE,fontSize=9.4,leading=12,spaceAfter=4)
CODE=ParagraphStyle('Code',parent=BASE,fontName='Consolas',fontSize=9,leading=12,spaceAfter=9)
heading_pages=[]
class ReportDoc(BaseDocTemplate):
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and f.style.name in ['H1','H2']:
   text=f.getPlainText()
   if text=='TABLE OF CONTENTS':return
   level=0 if f.style.name=='H1' else 1
   key='b'+str(self.seq.nextf('heading'))
   self.canv.bookmarkPage(key)
   self.canv.addOutlineEntry(text,key,level=level,closed=False)
   if level == 0: self.notify('TOCEntry',(level,text,self.page,key))
   heading_pages.append((text,self.page,level))
def decorate(c,d):
 if d.page==1:return
 c.saveState();c.setStrokeColor(colors.HexColor('#D9E1E6'));c.line(64,803,539,803)
 c.setFont('TimesNewRoman',8);c.setFillColor(colors.HexColor('#61717B'));c.drawRightString(539,811,'MITS GWALIOR | CENTRE OF ARTIFICIAL INTELLIGENCE')
 c.drawCentredString(298,27,str(d.page));c.restoreState()
T=TableOfContents();T.levelStyles=[ParagraphStyle('TOC0',fontName='TimesNewRoman',fontSize=10.5,leading=14,spaceBefore=6,leftIndent=0),ParagraphStyle('TOC1',fontName='TimesNewRoman',fontSize=9.5,leading=12,leftIndent=14)]
WIDTH=475

def para_flow(wp,maxw=WIDTH,incell=False):
 out=[]
 instr=' '.join(x.get(qn('w:instr'),'') for x in wp._p.xpath('.//w:fldSimple'))
 if instr.startswith('TOC '):return [T]
 for blip in wp._p.xpath('.//a:blip'):
  embed=blip.get(qn('r:embed'))
  if not embed:continue
  blob=doc.part.related_parts[embed].blob
  ext=wp._p.xpath('.//wp:extent')
  if ext:w=int(ext[0].get('cx'))/12700;h=int(ext[0].get('cy'))/12700
  else:w=maxw;h=maxw*.6
  ratio=min(1,maxw/w)
  img=Image(BytesIO(blob),width=w*ratio,height=h*ratio);img.hAlign='CENTER';out.append(img)
 txt=wp.text
 if txt.strip():
  sty=CELL if incell else BASE
  if wp.style.name=='Heading 1':sty=H1
  elif wp.style.name=='Heading 2':sty=H2
  elif wp.style.name=='Caption':sty=CAP
  elif wp.alignment==1:sty=CENTER
  elif any(r.font.name=='Consolas' for r in wp.runs):sty=CODE
  content=escape(txt).replace('\n','<br/>')
  if wp.runs and all(r.bold for r in wp.runs if r.text.strip()):content='<b>'+content+'</b>'
  sized=[r for r in wp.runs if r.font.size]
  if wp.style.name=='Normal' and sized and sty is not CODE:
   run=sized[0];size=run.font.size.pt
   color=colors.HexColor('#'+str(run.font.color.rgb)) if run.font.color.rgb else colors.black
   after=wp.paragraph_format.space_after.pt if wp.paragraph_format.space_after else 8
   sty=ParagraphStyle('ExplicitText',parent=CENTER if wp.alignment==1 else BASE,fontSize=size,leading=size*1.15,textColor=color,spaceAfter=after)
  out.append(Paragraph(content,sty))
 if wp._p.xpath('.//w:br[@w:type="page"]'):out.append(PageBreak())
 if wp._p.xpath('./w:pPr/w:sectPr'):out.append(PageBreak())
 return out

story=[]
skip_word_toc=False
for node in doc.element.body:
 if node.tag==qn('w:p'):
  wp=WP(node,doc)
  if wp.text.strip()=='TABLE OF CONTENTS':
   story+=para_flow(wp);story.append(T);skip_word_toc=True;continue
  if skip_word_toc:
   if wp.text.strip()=='LIST OF FIGURES AND TABLES':
    skip_word_toc=False;story.append(PageBreak())
   else:continue
  story+=para_flow(wp)
 elif node.tag==qn('w:tbl'):
  wt=WT(node,doc);n=len(wt.columns);data=[];hasimg=False
  for row in wt.rows:
   cells=[]
   for cell in row.cells:
    content=[]
    for wp in cell.paragraphs:
     if wp._p.xpath('.//a:blip'):hasimg=True
     content+=para_flow(wp,WIDTH/n-14,True)
    cells.append(content or [Paragraph('',CELL)])
   data.append(cells)
  t=Table(data,colWidths=[WIDTH/n]*n,repeatRows=0 if hasimg else 1,hAlign='CENTER')
  commands=[('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
  if not hasimg:commands += [('GRID',(0,0),(-1,-1),.45,colors.HexColor('#A7B8C4')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E8F1F3'))]
  t.setStyle(TableStyle(commands));story.extend([t,Spacer(1,9)])
# Avoid empty trailing pages.
while story and isinstance(story[-1],PageBreak):story.pop()
pdf=ReportDoc(str(R/'AR_Anatomy_Project_Report.pdf'),pagesize=(595.28,841.89),leftMargin=64,rightMargin=56,topMargin=49,bottomMargin=45,title='Satyam Anatomy AR - AR/VR Lab Project Report',author='Kartikey Tiwari; Satyam Pandey')
pdf.addPageTemplates(PageTemplate(id='main',frames=[Frame(64,45,WIDTH,747,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=decorate))
pdf.multiBuild(story)
# Cache PDF page entries in the editable Word TOC; Word can refresh after editing.
entries={}
for title,page,level in heading_pages:
 if level==0:entries[title]=page
for fld in doc.element.body.xpath('.//w:fldSimple'):
 if fld.get(qn('w:instr'),'').strip().startswith('TOC'):
  for child in list(fld):fld.remove(child)
  for title,page in entries.items():
   from docx.oxml import OxmlElement
   run=OxmlElement('w:r');text=OxmlElement('w:t');text.text=title+'  ...  '+str(page);run.append(text);fld.append(run)
   br=OxmlElement('w:r');line=OxmlElement('w:br');br.append(line);fld.append(br)
doc.save(R/'AR_Anatomy_Project_Report.docx')
print('PDF exported:',R/'AR_Anatomy_Project_Report.pdf')
