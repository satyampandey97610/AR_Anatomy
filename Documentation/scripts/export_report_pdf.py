from pathlib import Path
from io import BytesIO
from xml.sax.saxutils import escape
import hashlib
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph as WordParagraph
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,Image
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY,TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

R=Path(__file__).resolve().parents[1]
word=Document(R/'AR_Anatomy_Project_Report.docx')
for name,file in [('TimesNewRoman','times.ttf'),('TimesNewRoman-Bold','timesbd.ttf'),('TimesNewRoman-Italic','timesi.ttf'),('TimesNewRoman-BoldItalic','timesbi.ttf'),('Consolas','consola.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('TimesNewRoman',normal='TimesNewRoman',bold='TimesNewRoman-Bold',italic='TimesNewRoman-Italic',boldItalic='TimesNewRoman-BoldItalic')
BODY=ParagraphStyle('Body',fontName='TimesNewRoman',fontSize=12,leading=18,spaceAfter=6,alignment=TA_JUSTIFY,allowWidows=0,allowOrphans=0)
H1=ParagraphStyle('Heading1',parent=BODY,fontName='TimesNewRoman-Bold',fontSize=16,leading=18.4,spaceBefore=16,spaceAfter=8,alignment=TA_LEFT,keepWithNext=True)
H2=ParagraphStyle('Heading2',parent=BODY,fontName='TimesNewRoman-Bold',fontSize=13,leading=14.95,spaceBefore=16,spaceAfter=8,alignment=TA_LEFT,keepWithNext=True)
CAPTION=ParagraphStyle('Caption',parent=BODY,fontName='TimesNewRoman-Italic',fontSize=10,leading=11.5,spaceAfter=10,alignment=TA_CENTER)
CODE=ParagraphStyle('Code',parent=BODY,fontName='Consolas',fontSize=9,leading=12,spaceBefore=6,spaceAfter=8,alignment=TA_LEFT)
CONTENTS=TableOfContents();CONTENTS.levelStyles=[ParagraphStyle('TOC',fontName='TimesNewRoman',fontSize=11,leading=15,spaceBefore=5)]

def roman(value):
 result=''
 for number,letter in [(1000,'m'),(900,'cm'),(500,'d'),(400,'cd'),(100,'c'),(90,'xc'),(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]:
  while value>=number:result+=letter;value-=number
 return result

class ProjectReport(BaseDocTemplate):
 main_start=7
 def beforeDocument(self):self.entries=[]
 def afterFlowable(self,f):
  if not hasattr(f,'report_level'):return
  title=f.report_title;level=f.report_level
  if title=='CHAPTER 1: INTRODUCTION':self.main_start=self.page
  if title=='TABLE OF CONTENTS':return
  key='h'+hashlib.sha1(title.encode()).hexdigest()[:16]
  self.canv.bookmarkPage(key);self.canv.addOutlineEntry(title,key,level=level,closed=False)
  display=roman(self.page-1) if self.page<self.main_start else str(self.page-self.main_start+1)
  if level==0:
   self.notify('TOCEntry',(0,title,self.page,key));self.entries.append((title,display))

def page_furniture(c,d):
 if d.page==1:return
 c.saveState();c.setFont('TimesNewRoman',9);c.setFillColor(colors.black)
 c.drawRightString(538.59,805,'ANATOMY AR | AR/VR LAB')
 label=roman(d.page-1) if d.page<d.main_start else str(d.page-d.main_start+1)
 c.drawCentredString(297.64,35,label);c.restoreState()

story=[];cover=True
for node in word.element.body:
 if node.tag!=qn('w:p'):continue
 wp=WordParagraph(node,word)
 instruction=' '.join(x.get(qn('w:instr'),'') for x in node.xpath('.//w:fldSimple'))
 if instruction.strip().startswith('TOC'):
  story.append(CONTENTS);continue
 for blip in node.xpath('.//a:blip'):
  relation=blip.get(qn('r:embed'))
  if not relation:continue
  extent=node.xpath('.//wp:extent')[0]
  width=int(extent.get('cx'))/12700;height=int(extent.get('cy'))/12700
  limit=481.89 if cover else 453.54
  factor=min(1,limit/width)
  if wp.paragraph_format.space_before:story.append(Spacer(1,wp.paragraph_format.space_before.pt))
  img=Image(BytesIO(word.part.related_parts[relation].blob),width=width*factor,height=height*factor)
  img.hAlign='CENTER';img.keepWithNext=True;story.append(img)
 text=wp.text
 if text.strip():
  style=BODY
  if wp.style.name=='Heading 1':style=H1
  elif wp.style.name=='Heading 2':style=H2
  elif wp.style.name=='Caption':style=CAPTION
  elif wp.style.name=='Project Code':style=CODE
  if wp.alignment==1:
   style=ParagraphStyle(style.name+'Center',parent=style,alignment=TA_CENTER)
  sized=[r for r in wp.runs if r.font.size]
  if wp.style.name=='Normal' and sized:
   run=sized[0];size=run.font.size.pt
   color=colors.HexColor('#'+str(run.font.color.rgb)) if run.font.color.rgb else colors.black
   before=wp.paragraph_format.space_before.pt if wp.paragraph_format.space_before else 0
   after=wp.paragraph_format.space_after.pt if wp.paragraph_format.space_after else 0
   style=ParagraphStyle('CoverText',parent=style,fontSize=size,leading=size*1.15,textColor=color,spaceBefore=before,spaceAfter=after)
  content=escape(text).replace('\n','<br/>')
  runs=[r for r in wp.runs if r.text.strip()]
  if runs and all(r.bold for r in runs):content='<b>'+content+'</b>'
  flow=Paragraph(content,style)
  if wp.style.name in ['Heading 1','Heading 2']:
   flow.report_level=0 if wp.style.name=='Heading 1' else 1;flow.report_title=text
  story.append(flow)
 if node.xpath('.//w:br[@w:type="page"]'):story.append(PageBreak())
 if node.xpath('./w:pPr/w:sectPr'):
  story.append(PageBreak());cover=False
while story and isinstance(story[-1],PageBreak):story.pop()
report=ProjectReport(str(R/'AR_Anatomy_Project_Report.pdf'),pagesize=(595.28,841.89),title='Anatomy AR - AR/VR Lab Project Report',author='Kartikey Tiwari; Satyam Pandey')
cover_frame=Frame(56.69,56.69,481.90,728.51,id='cover',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
body_frame=Frame(85.04,70.87,453.55,700.15,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
report.addPageTemplates([PageTemplate(id='Cover',frames=[cover_frame],onPage=page_furniture,autoNextPageTemplate='Body'),PageTemplate(id='Body',frames=[body_frame],onPage=page_furniture)])
CONTENTS.formatter=lambda n: roman(n-1) if n<report.main_start else str(n-report.main_start+1)
report.multiBuild(story)
# Keep a readable TOC cache in Word; it can be updated after later edits.
for fld in word.element.body.xpath('.//w:fldSimple'):
 if fld.get(qn('w:instr'),'').strip().startswith('TOC'):
  for child in list(fld):fld.remove(child)
  for title,label in report.entries:
   run=OxmlElement('w:r');text=OxmlElement('w:t');text.text=title+'  ...  '+label;run.append(text);fld.append(run)
   run=OxmlElement('w:r');run.append(OxmlElement('w:br'));fld.append(run)
word.save(R/'AR_Anatomy_Project_Report.docx')
print('PDF saved:',R/'AR_Anatomy_Project_Report.pdf')
print('Main chapter starts on physical page:',report.main_start)
