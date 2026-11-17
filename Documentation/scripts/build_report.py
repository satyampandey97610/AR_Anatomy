from pathlib import Path
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH,WD_LINE_SPACING
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import json

ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'Documentation'
D=Document();s=D.sections[0]
s.page_width=Cm(21);s.page_height=Cm(29.7)
s.top_margin=Cm(2);s.bottom_margin=Cm(2);s.left_margin=Cm(2);s.right_margin=Cm(2)
normal=D.styles['Normal'];normal.font.name='Times New Roman';normal.font.size=Pt(12)
normal.paragraph_format.line_spacing=1.5;normal.paragraph_format.space_after=Pt(6)
normal.paragraph_format.widow_control=True
for name,size in [('Heading 1',16),('Heading 2',13)]:
 st=D.styles[name];st.font.name='Times New Roman';st.font.size=Pt(size);st.font.bold=True;st.font.color.rgb=RGBColor(0,0,0)
 st.paragraph_format.space_before=Pt(16);st.paragraph_format.space_after=Pt(8);st.paragraph_format.line_spacing=1.15;st.paragraph_format.keep_with_next=True
D.styles['Caption'].font.name='Times New Roman';D.styles['Caption'].font.size=Pt(10);D.styles['Caption'].font.italic=True
D.styles['Caption'].paragraph_format.line_spacing=1.15;D.styles['Caption'].paragraph_format.space_after=Pt(10)
code=D.styles.add_style('Project Code',1);code.font.name='Consolas';code.font.size=Pt(9)
code.paragraph_format.line_spacing_rule=WD_LINE_SPACING.EXACTLY;code.paragraph_format.line_spacing=Pt(12)
code.paragraph_format.space_before=Pt(6);code.paragraph_format.space_after=Pt(8)
D.core_properties.title='Anatomy AR - Project Report'
D.core_properties.author='Kartikey Tiwari; Satyam Pandey'
D.core_properties.subject='AR/VR Lab, Centre of Artificial Intelligence, MITS Gwalior'

def para(text='',center=False,bold=False):
 p=D.add_paragraph(text);p.alignment=WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
 if bold:
  for r in p.runs:r.bold=True
 return p

def h(text,level=1,center=False):
 p=D.add_heading(text,level)
 if center:p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 return p

def page():D.add_page_break()
def section(fmt):
 s=D.add_section(WD_SECTION_START.NEW_PAGE)
 s.left_margin=Cm(3);s.right_margin=Cm(2);s.top_margin=Cm(2.5);s.bottom_margin=Cm(2.5)
 s.header_distance=Cm(1.25);s.footer_distance=Cm(1.25)
 s.header.is_linked_to_previous=False;s.footer.is_linked_to_previous=False
 n=OxmlElement('w:pgNumType');n.set(qn('w:fmt'),fmt);n.set(qn('w:start'),'1');s._sectPr.append(n)
 p=s.header.paragraphs[0];p.text='ANATOMY AR | AR/VR LAB';p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
 for r in p.runs:r.font.name='Times New Roman';r.font.size=Pt(9)
 p=s.footer.paragraphs[0];p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'PAGE');p._p.append(f)
 return s

def cover(text,size=14,color='000000',before=0,after=8):
 p=para(text,True,True);p.paragraph_format.line_spacing=1.15;p.paragraph_format.space_before=Pt(before);p.paragraph_format.space_after=Pt(after)
 for r in p.runs:r.font.size=Pt(size);r.font.color.rgb=RGBColor.from_string(color)

cover('A',before=25)
cover('Project File For')
cover('AR-VR LAB')
cover('Anatomy AR',18,'0070C0')
cover('Submitted for the partial fulfilment of the degree of',12)
cover('Bachelor of Technology',18,'0070C0')
cover('In',12)
cover('Artificial Intelligence and Robotics',18,'0070C0',after=14)
cover('Submitted By',15,'7030A0',before=18)
cover('Kartikey Tiwari - 0901AI231033',13)
cover('Satyam Pandey - 0901AI231059',13)
cover('Submitted To',15,'7030A0',before=18)
cover('Dr. Vibha Tiwari',15,'997300')
cover('Mr. Ramnaresh Sharma',15,'984807')
cover('Centre of Artificial Intelligence',14)
p=D.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(36)
p.add_run().add_picture(str(OUT/'mits-header.jpeg'),width=Cm(16.5))
cover('July - Dec 2026',14,'0000FF',before=20)

section('lowerRoman')
h('DECLARATION BY THE CANDIDATES',center=True)
para('We, Kartikey Tiwari (0901AI231033) and Satyam Pandey (0901AI231059), submit this project report entitled “Anatomy AR” as part of the AR/VR Lab at the Centre of Artificial Intelligence, Madhav Institute of Technology & Science, Gwalior.')
para('The application is an adaptation of the AnatomyViewerAR project made available by danMoksh and collaborators. The original anatomy models, scenes, image-target data and tracking integration are acknowledged. The BSD 2-Clause license is retained in the source and in the application credits.')
para('This report explains the inherited application and the changes prepared for the present submission. These include the common interface, educational descriptions, inspection controls, build preparation and documentation. It records the available build checks and distinguishes Unity previews from phone-camera results.')
para('The sources used in preparing the project are listed in the references. Each member is responsible for understanding the application and explaining their actual contribution during the individual viva.')
para('\nKartikey Tiwari\n0901AI231033\nSignature: _______________________')
para('\nSatyam Pandey\n0901AI231059\nSignature: _______________________')
para('\nDate: __________________\nPlace: Gwalior')
page()
cover('MADHAV INSTITUTE OF TECHNOLOGY & SCIENCE, GWALIOR',13,after=4)
cover('(Deemed University)',12,after=4)
cover('Centre of Artificial Intelligence',12,after=12)
h('CERTIFICATE',center=True)
para('This project report entitled “Anatomy AR” is submitted by Kartikey Tiwari (0901AI231033) and Satyam Pandey (0901AI231059), students of the Centre of Artificial Intelligence, Madhav Institute of Technology & Science, Gwalior, for evaluation in the Augmented Reality / Virtual Reality Lab.')
para('The report describes an educational image-target augmented reality application developed by adapting an acknowledged existing project. It presents the application workflow, interface and interaction changes, Android build preparation, verification results and visual output.')
para('The report and working application are submitted to Dr. Vibha Tiwari and Mr. Ramnaresh Sharma for academic assessment. Faculty approval is indicated by the signatures below.')
para('\n\nDr. Vibha Tiwari\nFaculty Mentor\nSignature: _______________________')
para('\nMr. Ramnaresh Sharma\nFaculty Mentor\nSignature: _______________________')
para('\nDate: __________________')
page();h('ACKNOWLEDGEMENT',center=True)
para('We thank Dr. Vibha Tiwari and Mr. Ramnaresh Sharma for the opportunity to undertake and present this project in the AR/VR Lab. We acknowledge the academic support of the Centre of Artificial Intelligence at Madhav Institute of Technology & Science, Gwalior.')
para('We are grateful to danMoksh and the original AnatomyViewerAR team—Moksh Dandotiya, Yuvraj Tiwari and Mohit Sahu—for making the base project available. Their work supplied the anatomy content, original scenes and image-target application from which this adaptation began.')
para('We acknowledge the Unity and Vuforia documentation used to understand the development environment and tracking workflow. The reference project reports supplied for this assignment helped establish the required presentation format. Their project descriptions and screenshots have not been presented as results of our application.')
para('Preparing the submission required attention to both the visible demonstration and the supporting source, build and report. It provided an opportunity to understand how a stored model, a tracking reference and a user interface become a complete classroom application.')
para('\nKartikey Tiwari - 0901AI231033\nSatyam Pandey - 0901AI231059')
page();h('ABSTRACT',center=True)
para('Anatomy AR is an Android application for introductory anatomy visualization using image-target augmented reality. A user chooses a structure and points the phone camera at a configured picture. The application displays a stored three-dimensional model in relation to that reference. The included scenes cover the skeleton, skull, human body, heart and brain.')
para('The project adapts an existing Unity and Vuforia application. Unity manages the scenes, rendering and interface, while Vuforia provides the image-target integration. The adaptation adds a common menu, concise educational descriptions, size and reset controls, a rotation toggle, help and attribution. The target picture, source and APK are supplied with the project.')
para('The Android build completed successfully. Archive inspection, package metadata and v1/v2 signature checks were completed for the signed release. The original application was reported working on a Tecno Spark Go 2023. Final device validation of the adapted release remains a separate acceptance step. The report identifies the included scene images as Unity previews and does not treat them as phone-camera evidence.')
para('The project demonstrates the connection between recognition, tracking, rendering and interaction. It is intended for visual learning and practical explanation, rather than clinical use or reconstruction of arbitrary photographs.')
para('Keywords: augmented reality, image target, anatomy, Unity, Vuforia, Android, C#.')
page();h('TABLE OF CONTENTS',center=True)
f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),'TOC \\o "1-1" \\h \\z \\u');D.add_paragraph()._p.append(f)

section('decimal')

# Small, printable system diagram generated from the application workflow.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig,ax=plt.subplots(figsize=(9.3,2.1));ax.set_xlim(0,10);ax.set_ylim(0,2);ax.axis('off')
labels=['Choose a\\nmodel','Camera sees\\ntarget','Recognize\\nand track','Render\\nanatomy','Inspect and\\ninteract']
for i,label in enumerate(labels):
 x=.10+i*2
 box=FancyBboxPatch((x,.55),1.65,.9,boxstyle='round,pad=0.03',facecolor='#F1F4F6',edgecolor='#344654',linewidth=1)
 ax.add_patch(box);ax.text(x+.825,1,label.replace('\\n','\n'),ha='center',va='center',fontsize=10,fontfamily='serif')
 if i<4:ax.annotate('',xy=(x+1.94,1),xytext=(x+1.7,1),arrowprops={'arrowstyle':'->','color':'#344654'})
fig.savefig(OUT/'Output/System-Workflow.png',dpi=200,bbox_inches='tight',pad_inches=.12);plt.close(fig)

def picture(path,width,caption):
 p=D.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.keep_with_next=True;p.paragraph_format.space_after=Pt(4)
 p.add_run().add_picture(str(path),width=Cm(width))
 p=D.add_paragraph(caption,style='Caption');p.alignment=WD_ALIGN_PARAGRAPH.CENTER

output_data=[
('Main menu','OpenScene','The opening screen presents the five anatomy choices in one place. Model names are written as they appear to the user rather than as compact scene filenames. How to use opens the scanning instructions, while Credits contains the team and original-project acknowledgment. The app name is Anatomy AR.','The menu is the starting point for the demonstration. Selecting a structure loads its scene; it does not change which target picture is expected. This preview shows the implemented interface from Unity. The phone test should confirm that each button loads the correct scene and that the user can return to this screen.'),
('Skeleton scene','Skeleton','The skeleton scene introduces the supporting framework of the body. The stored model can be inspected from different viewpoints during the AR experience. The information panel briefly describes support, protection and movement, while the same inspection controls remain available at the bottom of the view.','The preview shows the scene content rather than a measured anatomical specimen. Size changes are presentation adjustments, and the model should not be used to infer a real bone measurement. In a phone demonstration, the learner first acquires the target and then moves slowly to inspect the visible structure.'),
('Skull scene','Skull','The skull model provides a compact example for the demonstration because its front and side surfaces are easy to distinguish. The information panel describes its role in protecting the brain and forming the framework of the face. The central viewing area is kept separate from navigation and the lower control panel.','This scene can be used to explain the difference between viewing an object and tracking the picture beneath it. The mesh supplies the visible shape, while the target provides the reference for placement. Pausing automatic rotation is intended to make a chosen view easier to inspect.'),
('Human-body scene','HumanBody','The human-body scene displays the inherited torso and head content, with visible internal structures. It provides an overview that complements the separate organ scenes. The educational description introduces the idea that organs and body systems work together rather than attempting to label every visible structure.','The asset is a prepared educational model. The application does not obtain this internal view by scanning a person. Its geometry and materials are stored in the project. This is an important point to explain in the viva because the camera is recognizing the configured picture, not performing a medical scan.'),
('Heart scene','Heart','The heart scene displays the stored heart model with the common navigation and inspection interface. The short description explains its pumping role and four chambers. The model offers a shape that can be viewed spatially, but the application does not include a patient-specific reconstruction or a clinically validated simulation of blood flow.','The scene also provides a straightforward example of the size and reset controls. The demonstrator can change the presentation, return to the captured starting transforms and pause or resume automatic rotation. These actions should be confirmed on the installed release before they are treated as passed device results.'),
('Brain scene','Brain','The brain scene completes the available model selection. Its description introduces coordination, sensory processing, memory and thought at a general level. The same menu, help, credits and inspection controls are used so that the learner can move between anatomy topics without learning a different interface.','The model is an introductory visual representation. Fine functional regions and clinical interpretation are outside the scope of this application. As with the other figures, this image was captured from Unity for documentation. A phone screenshot after the final test would add evidence of the actual camera overlay.')]

def outputs():
 page();h('CHAPTER 8: VISUAL OUTPUT')
 para('The following figures were captured from the actual Unity project. They show the stored models and implemented interface. They are scene previews, not screenshots of target tracking on the phone.')
 for i,(title,scene,before,after) in enumerate(output_data):
  if i:page()
  h('8.'+str(i+1)+' '+title,2)
  para(before)
  picture(OUT/'Output'/f'{scene}-UnityPreview.png',6.65,'Figure '+str(i+3)+'. '+title+' — Unity scene preview.')
  para(after)
 page()

text=(Path(__file__).parent/'report_content.md').read_text(encoding='utf-8')
workflow_count=None;target_count=None
for block in text.split('\n\n'):
 block=block.strip()
 if not block:continue
 if block.startswith('# '):
  title=block[2:]
  if title.startswith('CHAPTER 9:'):outputs()
  h(title)
 elif block.startswith('## '):
  title=block[3:];h(title,2)
  workflow_count=0 if title.startswith('4.1 ') else None
  target_count=0 if title.startswith('6.1 ') else None
 else:
  para(block.replace('\n',' '))
  if workflow_count is not None:
   workflow_count+=1
   if workflow_count==2:
    picture(OUT/'Output/System-Workflow.png',15.6,'Figure 1. Main application workflow.');workflow_count=None
  if target_count is not None:
   target_count+=1
   if target_count==2:
    picture(ROOT/'Demo/TARGET-PICTURE.png',6.4,'Figure 2. Configured image target supplied with the base project.');target_count=None

page();h('REFERENCES')
refs=[
'[1] danMoksh. AnatomyViewerAR: source, assets and BSD 2-Clause license. https://github.com/danMoksh/AnatomyViewerAR',
'[2] Unity Technologies. Unity 2018.2 Manual: Transform. https://docs.unity3d.com/2018.2/Documentation/Manual/class-Transform.html',
'[3] Unity Technologies. Unity 2018.2 Scripting API: Time.deltaTime. https://docs.unity3d.com/2018.2/Documentation/ScriptReference/Time-deltaTime.html',
'[4] PTC. Vuforia Engine: Best Practices for Designing and Developing Image-Based Targets. https://developer.vuforia.com/library/vuforia-engine/images-and-objects/image-targets/best-practices/best-practices-designing-and-developing-image-based-targets/',
'[5] PTC. Vuforia Engine: Image Targets. https://developer.vuforia.com/library/vuforia-engine/images-and-objects/image-targets/image-targets/',
'[6] Unity Technologies. Unity 2018.2.14f1 release and component downloads. https://unity.com/releases/editor/whats-new/2018.2.14f1',
'[7] Android Developers. apksigner. https://developer.android.com/tools/apksigner',
'[8] Madhav Institute of Technology & Science, Gwalior. Centre for Artificial Intelligence. https://web.mitsgwalior.in/academics/departments/centre-of-artificial-intelligence',
'[9] Anatomy AR. Adapted project source, release APK and build verification record. https://github.com/satyampandey97610/AR_Anatomy',
'[10] User-supplied reference reports: project_file_ar_vr.pdf; golf game final.pdf; pRACTICAL FILE ARVR.pdf; Project Report planets.docx; vr report.docx. Used as layout and submission-format references.'
]
for ref in refs:para(ref)

page();h('APPENDIX: SELECTED IMPLEMENTATION DETAILS')
h('A.1 Scene Loading',2)
para('The menu maps its buttons to scene names. The following call loads the Heart scene; that scene must also be included in the build list.')
p=D.add_paragraph('SceneManager.LoadScene("Heart");',style='Project Code')
h('A.2 Automatic Rotation',2)
para('The existing rotation script changes the Y-axis rotation during Update. Multiplying the speed by Time.deltaTime expresses an intended speed per second. The rotation toggle enables or disables this component.')
D.add_paragraph('void Update()\n{\n    transform.Rotate(0, 20 * Time.deltaTime, 0);\n}',style='Project Code')
h('A.3 Bounded Button-Based Scaling',2)
para('The common size multiplier is limited to a useful range. The captured initial scales are used as the reference for the model roots.')
D.add_paragraph('size = Mathf.Clamp(size * factor, 0.3f, 3f);\nfor (int i = 0; i < roots.Count; i++)\n{\n    if (roots[i])\n        roots[i].localScale = scales[i] * size;\n}',style='Project Code')
h('A.4 Resetting the Model Roots',2)
para('Reset restores the recorded local transforms and the default shared size multiplier. The code checks the Transform reference before accessing it.')
D.add_paragraph('size = 1f;\nfor (int i = 0; i < roots.Count; i++)\n{\n    if (!roots[i]) continue;\n    roots[i].localPosition = positions[i];\n    roots[i].localRotation = rotations[i];\n    roots[i].localScale = scales[i];\n}',style='Project Code')
h('A.5 Checking the Distributed Build',2)
v=json.loads((OUT/'BUILD-VERIFICATION.json').read_text(encoding='utf-8'))
para('The signed release is AnatomyAR.apk, version 1.0, with package identifier com.arvrlab.anatomyar. Its architecture is ARMv7. Archive inspection and Android v1/v2 signature verification passed. The checksum below identifies the distributed file.')
D.add_paragraph(v['sha256'],style='Project Code')
# Keep the editable file self-contained; the PDF exporter fills the TOC cache.
u=OxmlElement('w:updateFields');u.set(qn('w:val'),'false');D.settings.element.append(u)
path=OUT/'AR_Anatomy_Project_Report.docx';D.save(path)
print('DOCX saved:',path)
print('Tables:',len(D.tables),'body paragraphs:',len(D.paragraphs))
