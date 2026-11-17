from pathlib import Path
from docx import Document
from docx.shared import Inches,Pt,Cm,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import json

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'Documentation'
D=Document()
sec=D.sections[0]
sec.page_width=Cm(21);sec.page_height=Cm(29.7)
sec.top_margin=Cm(2);sec.bottom_margin=Cm(1.8);sec.left_margin=Cm(2.5);sec.right_margin=Cm(2)
for name in ['Normal','Body Text']:
 st=D.styles[name];st.font.name='Times New Roman';st.font.size=Pt(12)
 st.paragraph_format.line_spacing=1.15;st.paragraph_format.space_after=Pt(7)
for name,size in [('Title',24),('Heading 1',17),('Heading 2',13)]:
 st=D.styles[name];st.font.name='Times New Roman';st.font.size=Pt(size);st.font.color.rgb=RGBColor.from_string('17354A')
 st.paragraph_format.keep_with_next=True
D.styles['Caption'].font.name='Times New Roman';D.styles['Caption'].font.size=Pt(10)
D.core_properties.title='Satyam Anatomy AR - AR/VR Lab Project Report'
D.core_properties.author='Satyam Pandey; Kartikey Tiwari'
D.core_properties.subject='Centre of Artificial Intelligence, MITS Gwalior'

def p(text='',center=False,bold=False):
 q=D.add_paragraph(text);q.alignment=WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
 if bold:
  for r in q.runs:r.bold=True
 return q

def heading(text):D.add_heading(text,1)
def sub(text):D.add_heading(text,2)
def page():D.add_page_break()
def table(headers,rows):
 t=D.add_table(rows=1, cols=len(headers));t.style='Table Grid'
 for c,v in zip(t.rows[0].cells,headers):
  c.text=v
  for r in c.paragraphs[0].runs:r.bold=True
 for row in rows:
  for c,v in zip(t.add_row().cells,row):c.text=str(v)
 return t

def field(par,code):
 r=par.add_run();f=OxmlElement('w:fldSimple');f.set(qn('w:instr'),code);r._r.addnext(f)

def section(fmt):
 s=D.add_section(WD_SECTION_START.NEW_PAGE)
 s.header.is_linked_to_previous=False;s.footer.is_linked_to_previous=False
 n=OxmlElement('w:pgNumType');n.set(qn('w:fmt'),fmt);n.set(qn('w:start'),'1');s._sectPr.append(n)
 hp=s.header.paragraphs[0];hp.text='AR/VR LAB  |  ANATOMY AR';hp.alignment=WD_ALIGN_PARAGRAPH.RIGHT
 hp.runs[0].font.size=Pt(9);hp.runs[0].font.color.rgb=RGBColor.from_string('61717B')
 fp=s.footer.paragraphs[0];fp.alignment=WD_ALIGN_PARAGRAPH.CENTER;field(fp,'PAGE')
 return s

# Cover follows the supplied institutional project-report format.
D.add_picture(str(OUT/'mits-header.jpeg'),width=Cm(16.5))
p('\nPROJECT REPORT\nON',True,True)
q=p('Satyam Anatomy AR',True,True)
for r in q.runs:r.font.size=Pt(23)
p('Interactive Human Anatomy Learning\nUsing Augmented Reality',True,True)
p('Augmented Reality / Virtual Reality Lab',True)
p('Submitted in partial fulfilment of the academic requirements\nfor the degree of Bachelor of Technology',True)
p('\nSubmitted By',True,True)
table(['Student','Enrollment Number'],[['Kartikey Tiwari','0901AI231033'],['Satyam Pandey','0901AI231059']])
p('\nSubmitted To',True,True)
p('Dr. Vibha Tiwari\nMr. Ramnaresh Sharma',True)
p('CENTRE OF ARTIFICIAL INTELLIGENCE',True,True)
p('MADHAV INSTITUTE OF TECHNOLOGY & SCIENCE, GWALIOR\n(Deemed University)\nGola Ka Mandir, Gwalior - 474005, Madhya Pradesh',True)
p('November 2026',True,True)

section('lowerRoman')
heading('DECLARATION BY THE CANDIDATES')
p('We, Kartikey Tiwari (0901AI231033) and Satyam Pandey (0901AI231059), submit this report entitled “Satyam Anatomy AR: Interactive Human Anatomy Learning Using Augmented Reality” for evaluation in the AR/VR Lab at the Centre of Artificial Intelligence, Madhav Institute of Technology & Science, Gwalior.')
p('The project is an adaptation of the publicly available AnatomyViewerAR project by danMoksh and collaborators. The original anatomy models, image-target data, scenes and relevant source are acknowledged. The original BSD 2-Clause license is retained. This report distinguishes inherited functionality from the interface, interaction, build and documentation changes included in the adaptation.')
p('We understand that the project demonstration and our individual understanding will be evaluated. Build results, preview images and device observations are identified according to their actual source. Pending device tests are not represented as completed tests.')
p('\nKartikey Tiwari - 0901AI231033\nSignature: __________________________')
p('\nSatyam Pandey - 0901AI231059\nSignature: __________________________')
p('\nDate: __________________\nPlace: Gwalior')
page();heading('CERTIFICATE')
p('This project report entitled “Satyam Anatomy AR: Interactive Human Anatomy Learning Using Augmented Reality” is submitted by Kartikey Tiwari (0901AI231033) and Satyam Pandey (0901AI231059), students of the Centre of Artificial Intelligence, Madhav Institute of Technology & Science, Gwalior (Deemed University), for evaluation in the Augmented Reality / Virtual Reality Lab.')
p('The work presents an educational image-target AR application based on an acknowledged existing project, together with interface and interaction adaptations, Android build preparation and project documentation. Approval of the report and assessment of the working demonstration are subject to faculty verification.')
p('\n\nDr. Vibha Tiwari\nFaculty Mentor\nSignature: __________________________')
p('\n\nMr. Ramnaresh Sharma\nFaculty Mentor\nSignature: __________________________')
p('\nCentre of Artificial Intelligence\nMadhav Institute of Technology & Science, Gwalior')
p('\nDate: __________________')
page();heading('ACKNOWLEDGEMENT')
p('We express our thanks to Dr. Vibha Tiwari and Mr. Ramnaresh Sharma for the opportunity to undertake and present this AR/VR Lab project. We acknowledge the academic support of the Centre of Artificial Intelligence at Madhav Institute of Technology & Science, Gwalior.')
p('We acknowledge danMoksh and the original AnatomyViewerAR team—Moksh Dandotiya, Yuvraj Tiwari and Mohit Sahu—for the base project. Their work provided the anatomy content and original image-target application on which this adaptation is based.')
p('We also acknowledge Unity Technologies and the Vuforia Engine developers for the tools and documentation used to understand the application. The reference reports supplied for this submission were used for report structure and presentation, not as evidence of our project outputs.')
p('\nKartikey Tiwari - 0901AI231033\nSatyam Pandey - 0901AI231059')
page();heading('ABSTRACT')
p('Satyam Anatomy AR is an Android educational application that displays three-dimensional anatomy models in relation to a predefined image viewed through a phone camera. The project demonstrates the practical use of image-target augmented reality for inspecting the skeleton, skull, human body, heart and brain. It does not reconstruct models from arbitrary photographs; the models are stored within the application.')
p('The implementation adapts an existing Unity and Vuforia project. Unity manages scenes, models, interface elements and Android packaging, while Vuforia supplies image recognition and tracking. The adaptation adds a consistent model-selection menu, concise educational descriptions, bounded size controls, reset, pause/resume rotation, help and attribution. The application name is used without repeatedly branding every viewer screen.')
p('The adapted Android build was compiled successfully, its package metadata was inspected, and its APK archive and Android v1/v2 signatures were verified. The original APK was reported working on a Tecno Spark Go 2023. The new build still requires device testing; compatibility with a future Realme device has not been established. Output figures in this report are identified as Unity previews rather than phone-camera tracking evidence.')
p('Keywords: augmented reality, image target, anatomy visualization, Unity, Vuforia, Android, C#.')
page();heading('TABLE OF CONTENTS')
field(D.add_paragraph(),'TOC \\o "1-2" \\h \\z \\u')
p('The table of contents is generated from the report headings. Page numbers are updated when the document is exported to PDF.')
page();heading('LIST OF FIGURES AND TABLES')
p('Figure 1. Image-target application workflow.\nFigure 2. Required tracking target supplied with the base project.\nFigures 3–8. Unity previews of the menu and anatomy scenes.\nFigure 9. Android build and package verification summary.')
p('Tables cover objectives, development tools, modules, interaction behavior, verification results, demonstration steps and viva preparation. The phone-camera output of the adapted APK must be added after the presentation-device test.')

section('decimal')
heading('CHAPTER 1: INTRODUCTION')
sub('1.1 Background')
p('Anatomy is commonly introduced using static diagrams and textbook illustrations. These resources are useful, but a single flat view can make the spatial arrangement of a structure difficult to inspect. A three-dimensional model allows the viewer to examine shape and relative position from different viewpoints. Augmented reality connects that digital model with a visible reference in the real environment.')
p('In this project, a phone camera observes a predefined picture. The image-tracking system recognizes that reference and estimates its position and orientation. Unity renders an anatomy model in alignment with it. The learner sees the real camera image and the digital model together on the phone screen. No physical hologram is projected into the room.')
sub('1.2 AR and VR Concepts')
table(['Concept','Meaning','Relation to this project'],[['Augmented reality','Digital content is added to a view of the real environment.','The anatomy model is aligned with an image target in the camera view.'],['Virtual reality','A virtual environment occupies the user’s view, commonly through a tracked headset.','A headset-based VR environment is outside this project’s scope.'],['3D rendering','A geometric model is drawn from a virtual camera viewpoint.','Unity renders the stored anatomy models.']])
sub('1.3 Problem Statement')
p('The practical problem is to create a demonstrable educational AR application that is understandable to first-time users and suitable for a classroom viva. The application should provide a clear route from selecting a model to scanning the target and inspecting the resulting content. Its report should accurately explain the technology and the students should be able to demonstrate the workflow independently.')
sub('1.4 Objectives and Scope')
table(['Objective','Implementation scope'],[['Recognize a known reference','Use the configured Skleton image target and packaged database.'],['Present anatomy content','Provide skeleton, skull, human-body, heart and brain scenes.'],['Support inspection','Offer navigation, size, reset and automatic-rotation controls.'],['Explain the content','Display short educational descriptions and usage instructions.'],['Prepare a practical submission','Provide source, APK, target, report and viva guidance with attribution.']])
p('The application is an educational visualization tool. It is not intended for diagnosis, treatment planning, patient-specific anatomy or measurement of biological structures. Improved learning outcomes are a possible benefit to investigate, not a result established by this implementation.')

page();heading('CHAPTER 2: DEVELOPMENT TOOLS AND ASSETS')
sub('2.1 Software Environment')
table(['Tool','Role'],[['Unity 2018.2.14f1','Original project editor; scenes, rendering, UI and Android build.'],['Vuforia bundled support','Image-target recognition, tracking and camera integration.'],['C#','Navigation, presentation and interaction scripts.'],['JDK 8','Java tools used by the legacy Android packaging process.'],['Android SDK platform 28 and build-tools 28.0.3','Resource compilation, APK inspection, alignment and signing.'],['Git and GitHub','Source version control, documentation and release downloads.']])
p('The project uses a legacy editor/runtime to preserve the original application setup. Simply opening it in a current Unity editor does not guarantee compatibility. A supported ARM64 runtime would require a separate migration and validation effort.')
sub('2.2 Hardware and Device Requirements')
p('Development was prepared on a Windows laptop with 24 GB RAM. The classroom demonstration requires an Android phone with a functioning camera, permission to use that camera, and the supplied image target on paper or another screen. A VR headset is not required.')
p('The existing APK was reported working on a Tecno Spark Go 2023. The adapted build is ARMv7 with minimum SDK 23 and target SDK 28. These settings describe the package; they do not prove compatibility with every Android phone. A Realme device must be tested separately, especially if it accepts only ARM64 applications.')
sub('2.3 Models, Materials and Tracking Assets')
p('The anatomy meshes, textures, materials, original scenes and target database are inherited from AnatomyViewerAR. The tracking database is packaged under Assets/StreamingAssets/Vuforia. The configured target is named Skleton in AR_Demo.xml. Scene selection determines which stored anatomy content is displayed; it does not change the app into a general image-recognition or photo-reconstruction system.')
p('Original project credits and the BSD 2-Clause license are retained. Individual third-party assets may have their own conditions. The presence of an asset in the base repository is not a claim that this team created it.')

page();heading('CHAPTER 3: SYSTEM DESIGN AND WORKING PRINCIPLE')
sub('3.1 Application Workflow')
table(['Stage','Action'],[['1. Select','The user selects an anatomy scene from the main menu.'],['2. Observe','The phone camera supplies frames to the tracking system.'],['3. Recognize','Vuforia looks for features corresponding to the configured target.'],['4. Track','The target pose is estimated as the phone or target moves.'],['5. Render','Unity displays the stored anatomy model in alignment with the target.'],['6. Interact','The user changes size, resets the model, pauses rotation or returns to the menu.']])
p('Figure 1. Image-target application workflow: selection → camera observation → recognition → pose tracking → rendering → interaction.',center=True)
sub('3.2 Recognition, Tracking and Rendering')
p('Recognition answers which configured target is visible. Tracking estimates where that target is and how it is oriented over time. Rendering uses the virtual camera, model geometry, materials and lighting to draw the digital object. These are related stages, but they are not the same operation.')
p('The ImageTarget object provides a parent reference for model transforms. A Transform stores position, rotation and scale. Local transforms describe the model relative to its parent, which allows the model to follow the target reference. Menu and information elements are displayed through a Unity Canvas.')
sub('3.3 Modules')
table(['Module','Responsibility'],[['Menu and scene navigation','Select and load anatomy scenes.'],['Camera and target tracking','Acquire the camera image and maintain a target reference.'],['Anatomy rendering','Display model geometry and materials.'],['Educational interface','Show names, short facts and instructions.'],['Model controls','Change size, restore transforms and pause/resume rotation.'],['Build and distribution','Compile the Android package, sign it and publish release assets.']])

page();heading('CHAPTER 4: IMPLEMENTATION')
sub('4.1 Existing Project and Adaptation')
p('The base repository supplied the anatomy scenes, model content and Vuforia integration. The adaptation focuses on the user-facing workflow and preparation of a reproducible classroom build. The original source is acknowledged in the README, report, license and in-app Credits.')
p('The legacy canvas is replaced at scene startup by a consistent generated interface. The app name appears on the menu, while viewer screens use the neutral label Anatomy AR. The interface offers the five model choices, instructions, team information and source attribution.')
sub('4.2 Navigation and Educational Content')
p('Each anatomy choice loads its corresponding Unity scene. A short information panel describes the selected structure. The heart panel explains its pumping role and four chambers; the skull panel explains protection of the brain; other panels introduce the skeleton, body and brain. The descriptions are introductory and do not establish clinical completeness.')
sub('4.3 Size, Reset and Rotation Controls')
p('The size buttons multiply the initial model-root scale by a factor clamped between 0.3 and 3. Reset restores the captured local position, rotation and scale of the model roots. The automatic-rotation toggle enables or disables the existing Rotate components. Pinch interaction guards against a missing selection, an invalid starting distance and touches that begin over interface controls.')
table(['Control','Intended behavior'],[['Smaller / Larger','Apply a bounded size multiplier to model roots.'],['Reset','Restore captured initial root transforms.'],['Pause / Resume rotation','Disable or enable automatic Rotate components.'],['Menu','Load the opening model-selection scene.'],['Help / Credits','Display instructions and project attribution.']])
sub('4.4 Build Compatibility Fixes')
p('An unused model-recognition sample handler did not match the bundled Vuforia API. It was removed and its editor attachment hook adjusted for this image-target application. The legacy Android build initially waited on an online Gradle dependency. The final packaging route used Unity’s internal Android build method and the installed SDK tools.')
p('The generated package was aligned and signed using Android build tools. Signing is a necessary packaging step: a successful Unity build message alone does not establish that an APK is installable. Android v1 and v2 signature verification was completed for the distributed file.')
sub('4.5 Important Source Files')
table(['File','Purpose'],[['SatyamAnatomyUI.cs','Menu, facts, model controls, instructions and credits.'],['Rotate.cs','Automatic rotation using Time.deltaTime.'],['CSharpscaling.cs','Guarded two-touch scaling.'],['LoadGame.cs','Scene navigation and quitting.'],['SatyamBuild.cs','Android build configuration.'],['ReportPreview.cs','Clearly labeled Unity output previews for documentation.']])

page();heading('CHAPTER 5: INSTALLATION AND DEMONSTRATION')
sub('5.1 Installing the Application')
p('Download SatyamAnatomyAR.apk from the project’s v1.0.0 GitHub release. Open it on the Android phone and follow the installation prompt if the operating system permits it. Open the application and allow camera access. This package has its own application ID, com.satyampandey.anatomyar, so it is distinguishable from the original application.')
p('Repository: https://github.com/satyampandey97610/AR_Anatomy\nAPK release: https://github.com/satyampandey97610/AR_Anatomy/releases/tag/v1.0.0')
sub('5.2 Preparing the Image Target')
p('Display Demo/TARGET-PICTURE.png on a laptop or print it without distorting the proportions. Keep the complete picture visible to the camera. Use even lighting, a flat surface and minimal glare. Select a model before scanning. A random anatomy photograph will not substitute for the configured target.')
D.add_picture(str(ROOT/'Demo/TARGET-PICTURE.png'),width=Cm(7.7))
D.add_paragraph('Figure 2. Required tracking target inherited from the original project.',style='Caption')
sub('5.3 Viva Demonstration Sequence')
p('Introduce the educational purpose, open the menu, select a model, scan the target, move the phone to inspect the model and show the controls. Explain the roles of Unity, Vuforia and the target database. State the inherited content and the adaptation honestly. Both students should rehearse the complete demonstration.')

page();heading('CHAPTER 6: VERIFICATION AND RESULTS')
sub('6.1 Build and Package Verification')
table(['Check','Result'],[['Unity Android compilation and packaging','Passed; build completed successfully.'],['APK archive integrity','Passed; no corrupt ZIP entry found.'],['Application label','Satyam Anatomy AR.'],['Application identifier','com.satyampandey.anatomyar.'],['Android configuration','Minimum API 23; target API 28; ARMv7.'],['Android v1 / v2 signatures','Verified for the distributed signed APK.'],['Original APK on Tecno','User reported working anatomy views.'],['New adapted APK on Tecno','Pending phone validation.'],['Realme device compatibility','Not tested.']])
verification=json.loads((OUT/'BUILD-VERIFICATION.json').read_text())
p('Distributed APK SHA-256:\n'+verification['sha256'])
D.add_paragraph('Figure 9. Package verification summary; the hash identifies the signed release APK.',style='Caption')
sub('6.2 Device Acceptance Checklist')
p('For the final phone test, record the exact phone model, installed Android version and APK version. Check launch, camera permission, target acquisition, target loss and recovery, all five model scenes, navigation, size controls, reset, rotation, help, credits and close/reopen. Any error should be recorded rather than replaced by an assumed pass.')
p('A screen recording and phone screenshots should be retained after this test. They will provide evidence of the actual camera overlay and can replace or supplement the clearly labeled Unity previews in the next chapter. The original app’s success is useful baseline evidence but is not a substitute for testing the adapted APK.')
sub('6.3 Interpretation of Results')
p('The completed checks establish that the adaptation compiles and that its release package has valid signatures and expected metadata. They do not establish runtime camera performance or universal hardware compatibility. Those conclusions require testing the installed release on the intended demonstration phone.')

page();heading('CHAPTER 7: SCREENSHOTS AND VISUAL OUTPUT')
p('The figures below are captured from the project in Unity with the models and presentation interface prepared for preview. They are not photographs or screenshots of successful camera tracking on the phone. Their purpose is to show model content and interface output without inventing a device-test result.')
images=[('OpenScene','Main menu'),('Skeleton','Skeleton scene'),('Skull','Skull scene'),('HumanBody','Human-body scene'),('Heart','Heart scene'),('Brain','Brain scene')]
for pair in range(0,len(images),2):
 if pair:page()
 t=D.add_table(rows=1,cols=2)
 for cell,(scene,title) in zip(t.rows[0].cells,images[pair:pair+2]):
  path=OUT/'Output'/f'{scene}-UnityPreview.png'
  if path.exists():cell.paragraphs[0].add_run().add_picture(str(path),width=Cm(7.2))
  cap=cell.add_paragraph(f'Figure {3+images.index((scene,title))}. {title} — Unity preview.');cap.style=D.styles['Caption']
 p('Output source: project-generated Unity preview. Adapted APK phone-camera screenshots are pending the device test.',center=True)

page();heading('CHAPTER 8: LIMITATIONS, FUTURE SCOPE AND CONCLUSION')
sub('8.1 Limitations')
p('Tracking quality depends on target visibility, lighting, glare, camera focus and device behavior. The anatomy assets and descriptions are simplified educational representations. The system does not scan internal organs, identify arbitrary pictures or generate patient-specific models. The legacy ARMv7 runtime limits compatibility with devices that require ARM64 applications.')
sub('8.2 Future Scope')
p('Future work can include migration to a supported Unity/Vuforia runtime, ARM64 builds, detailed structure labels, accessible controls, improved content provenance records and a small knowledge quiz. A user study could compare learning outcomes with conventional illustrations. These are proposed extensions, not features claimed in the submitted build.')
sub('8.3 Individual Understanding and Team Preparation')
table(['Student','Enrollment','Viva preparation'],[['Kartikey Tiwari','0901AI231033','Explain the AR workflow, target, scene content and the complete demonstration.'],['Satyam Pandey','0901AI231059','Explain project adaptation, interface controls, build setup and the complete demonstration.']])
p('Each student should confirm and describe the work they actually performed. Shared preparation should cover the full application so that either member can demonstrate it. This table identifies preparation responsibilities and does not invent unobserved development contributions.')
sub('8.4 Conclusion')
p('The project demonstrates an image-target approach to anatomy visualization using Unity and Vuforia. The adaptation provides a clearer selection and inspection workflow, educational descriptions and retained attribution. Android compilation, package inspection and signature verification were completed. Final phone testing and live AR screenshots remain the acceptance step before the viva submission is treated as fully validated.')

page();heading('REFERENCES')
refs=[
'[1] danMoksh, AnatomyViewerAR source repository and BSD 2-Clause license. https://github.com/danMoksh/AnatomyViewerAR',
'[2] Unity Technologies, Unity 2018.2.14f1 release and component downloads. https://unity.com/releases/editor/whats-new/2018.2.14f1',
'[3] Unity Technologies, Unity Manual and Scripting API. https://docs.unity3d.com/',
'[4] PTC, Vuforia Engine Image Targets. https://developer.vuforia.com/library/vuforia-engine/images-and-objects/image-targets/image-targets/',
'[5] PTC, Vuforia Engine Supported Versions. https://developer.vuforia.com/library/vuforia-engine/platform-support/supported-versions/',
'[6] Madhav Institute of Technology & Science, Gwalior, Centre for Artificial Intelligence. https://web.mitsgwalior.in/academics/departments/centre-of-artificial-intelligence',
'[7] Android Developers, apksigner documentation. https://developer.android.com/tools/apksigner',
'[8] Reference reports supplied by the user: project_file_ar_vr.pdf; golf game final.pdf; pRACTICAL FILE ARVR.pdf; Project Report planets.docx; vr report.docx. Used for layout and report structure.',
'[9] Submission repository and release. https://github.com/satyampandey97610/AR_Anatomy'
]
for x in refs:p(x)
page();heading('APPENDIX A: IMPORTANT CODE AND EXPLANATION')
sub('A.1 Frame-Rate-Independent Rotation')
p('The existing Rotate script rotates its object around the Y-axis. Time.deltaTime represents elapsed frame time, so the intended angular speed is expressed per second rather than per frame.')
q=p('void Update()\n{\n    transform.Rotate(0, 20 * Time.deltaTime, 0);\n}')
for r in q.runs:r.font.name='Consolas';r.font.size=Pt(10)
sub('A.2 Bounded Size Control')
p('The adaptation captures the original model-root scales and applies a common bounded multiplier. This makes the button-based size control easier to explain and reset.')
q=p('size = Mathf.Clamp(size * factor, 0.3f, 3f);\nfor (int i = 0; i < roots.Count; i++)\n    if (roots[i])\n        roots[i].localScale = scales[i] * size;')
for r in q.runs:r.font.name='Consolas';r.font.size=Pt(10)
sub('A.3 Scene Navigation')
p('SceneManager.LoadScene loads the selected anatomy scene. The scene names must match the scenes included in the build.')
q=p('SceneManager.LoadScene("Heart");')
for r in q.runs:r.font.name='Consolas';r.font.size=Pt(10)
p('The complete implementation is included in the repository. Code excerpts in this appendix explain selected concepts and are not a replacement for reading the full source.')
page();heading('APPENDIX B: SIMPLE VIVA QUESTIONS')
qa=[('What is this project?','An Android app that displays stored anatomy models aligned with a predefined picture in the camera view.'),('Why is it AR?','The digital model is displayed in relation to a real target seen through the camera.'),('What does Vuforia do?','It recognizes and tracks the configured target.'),('What does Unity do?','It manages scenes, rendering, interface, scripts and builds.'),('Does any picture work?','No. The configured tracking target is required.'),('Did you create everything from scratch?','No. The existing project and assets are acknowledged; explain the actual adaptations.'),('What does reset do?','It restores captured initial local model-root transforms.'),('Is it guaranteed to work on every phone?','No. Architecture and runtime compatibility must be tested.'),('What is the main remaining check?','Install and test the signed adapted APK on the actual viva phone.')]
for a,b in qa:sub(a);p(b)
# Request field refresh when opened in Word.
settings=D.settings.element;u=OxmlElement('w:updateFields');u.set(qn('w:val'),'true');settings.append(u)
path=OUT/'AR_Anatomy_Project_Report.docx';D.save(path)
print(path)
