# CHAPTER 1: INTRODUCTION

## 1.1 Introduction to the Project

Anatomy AR is an Android application for viewing human anatomy models through augmented reality. The user selects a structure, points the phone camera at a particular picture and sees a stored three-dimensional model aligned with that picture. The project includes the skeleton, skull, human body, heart and brain. Its purpose is to make the shape of these structures easier to inspect during an introductory classroom demonstration.

A printed anatomy diagram presents a fixed view. A learner can read its labels, but cannot change the viewing angle of the drawing. A three-dimensional model provides another way to study shape: the learner can look at its front, side and other visible surfaces. In this application, the target picture supplies a reference in the physical environment. Moving the phone changes the view of the digital content relative to that reference.

The phone screen remains the display throughout the experience. The application does not project a physical hologram into the room. It combines a camera view with a rendered object, so the learner sees the real picture and digital anatomy together. This relationship between the physical reference and the digital model is the main AR concept demonstrated by the project.

## 1.2 Problem Statement

The laboratory requirement is to present one functional AR or VR project and explain the concepts, tools and individual contributions involved. A useful project for this purpose must have a clear demonstration sequence and a manageable hardware requirement. It must also be possible to inspect its source and connect the visible behavior to the underlying implementation.

The problem addressed here is the presentation of anatomy models through a simple image-target workflow. The user should be able to choose a structure, understand which picture to scan, view the model and return to the menu without needing to understand the development tools. The accompanying report should explain how recognition, tracking, rendering and interaction fit together.

## 1.3 Objectives

The first objective is to recognize a predefined image target and use it as the reference for anatomy content. The second is to provide five anatomy scenes in a common application. The third is to make inspection easier through size controls, a reset function and a rotation toggle. Short descriptions and a help screen support users who are opening the application for the first time.

The practical submission also requires a build that can be identified and checked. For this reason, the adapted application has its own package identifier, an installable Android release, source files and supporting documentation. Original content is acknowledged so that the adaptation can be explained accurately during the viva.

## 1.4 Scope of the Work

The project is limited to stored educational models and a configured tracking image. It is not a system for converting arbitrary photographs into three-dimensional objects. It does not scan the inside of a person, produce patient-specific anatomy or support clinical diagnosis. The anatomy descriptions introduce the structures; they are not a replacement for an anatomy textbook or professional medical instruction.

The implementation starts from the AnatomyViewerAR repository supplied as a possible senior project. The inherited scenes, assets and tracking integration are retained. The adaptation changes the presentation, adds educational and inspection controls, resolves build compatibility issues and prepares the source, APK and report for a laboratory submission. These boundaries are important when explaining what was reused and what changed.

# CHAPTER 2: BACKGROUND AND CHOICE OF APPROACH

## 2.1 Augmented Reality and Virtual Reality

Augmented reality places digital content in relation to a view of the real environment. A mobile AR application commonly uses a camera to observe the environment and a display to show the combined result. Recognition and tracking supply the information needed to maintain a useful relationship between the observed reference and the digital content.

Virtual reality presents a virtual environment as the user's view, commonly through a headset. Head tracking changes the viewpoint as the user turns, and controllers or other input methods allow interaction. A normal three-dimensional application on a monitor is not automatically a headset-based VR experience. The way the viewpoint is presented and tracked matters as much as the presence of a 3D model.

Anatomy AR uses the AR approach. The user continues to see the target picture through the camera. The stored anatomy model is added to that view. No headset is required for the proposed demonstration, which makes the workflow suitable for showing the application directly on a phone display.

## 2.2 Image-Target AR

An image target is a picture configured for recognition by the tracking system. The application does not treat every visible picture as a valid target. The reference must correspond to the target information available to the application. In this project, the database file AR_Demo.xml identifies a target named Skleton. The supplied target picture is therefore part of the demonstration equipment, not just an illustration in the report.

Recognition and tracking have different roles. Recognition establishes that the configured reference has been found. Tracking estimates its position and orientation as the camera view changes. The rendering system uses this changing reference to display the model. A model can be stored correctly in the application and still fail to appear as expected if the wrong picture is scanned or the target cannot be tracked.

Good image targets contain distinguishable visual features. Vuforia's image-target guidance recommends feature-rich imagery, useful contrast and features distributed across the picture [4]. These properties help explain why a plain blank card or an unrelated photograph should not be substituted for the supplied target. Lighting, focus, glare and the amount of the picture visible to the camera also affect the practical scanning conditions.

## 2.3 Static Diagrams, 3D Viewers and AR

A textbook diagram is convenient to print and annotate. It remains useful when a learner needs clear labels or a particular sectional view. A conventional 3D viewer adds the ability to change the model viewpoint on a screen. Image-target AR adds a physical reference to that inspection process, allowing the user to move a phone around a visible picture while viewing the associated content.

These approaches serve related purposes rather than forming a measured ranking. The present project does not include a controlled comparison of learning outcomes. Its educational value is demonstrated through the available interaction and visual inspection, while any claim of improved examination performance would require a separate user study.

## 2.4 Reason for Selecting the Anatomy Project

The anatomy project offers a clear starting and ending point for a viva demonstration: select a model, scan a known picture, inspect the model and explain the technology. It also has an application that could be tested on an available Android phone before modifying the source. The original APK was reported working on the Tecno Spark Go 2023 used for the initial check.

The main difficulty was the age of the development environment. The repository identifies Unity 2018.2.14f1 and uses a bundled Vuforia integration. Choosing this project therefore required attention to matching build tools and package compatibility. The existing working application was treated as a baseline, while the adapted version was given separate build and verification records.

# CHAPTER 3: REQUIREMENTS AND DEVELOPMENT ENVIRONMENT

## 3.1 Functional Requirements

The application must provide a menu from which the user can select an anatomy scene. Opening a scene must give access to the camera-based experience and an explanation of the selected structure. The user must be able to return to the menu, open instructions and read the project credits. These operations form the basic navigation requirements.

Within a model scene, the interface supplies smaller and larger controls, a reset function and a pause/resume control for automatic rotation. The size controls are intended for inspection, not for anatomical measurement. Reset restores the captured initial transforms of the model roots. The interface should use the same control arrangement in each anatomy scene so that the user does not have to learn five different workflows.

The target picture, source code and installable application must accompany the report. A successful demonstration depends on having the correct picture available as well as the phone application. The repository therefore includes a Demo folder with the target image and a simple local page for displaying it on a laptop.

## 3.2 Usability and Reliability Requirements

The opening screen should make the available models easy to identify. Help should explain that a particular picture is required, because a new user may otherwise assume that any image of a body part can be scanned. Controls should remain distinguishable from the model area and use familiar words such as Menu, Help and Reset.

The application must be checked on the actual presentation device. A package that builds successfully on a laptop is not automatically verified on every phone. Camera permission, device architecture, operating-system behavior and the legacy AR runtime all affect the final result. Reliability for the viva therefore includes a repeatable device test and a clear record of the APK used.

## 3.3 Unity and C#

Unity manages the scenes, game objects, camera, materials, lighting, interface and Android packaging. A scene stores an arrangement of objects and their components. A GameObject acts as a container for those components. The Transform records position, rotation and scale, while components such as a Renderer or a script provide other behavior [2].

C# scripts connect the user interface to the application logic. In this project, scripts load scenes, create the common interface, adjust model transforms and control automatic rotation. The scripts are relatively small compared with the engine and tracking SDK. This distinction is useful during the viva: the application uses an existing tracking engine rather than implementing image matching from first principles.

## 3.4 Vuforia and the Android Tools

Vuforia provides the camera and image-target tracking integration used by the inherited project. The target database is stored with the application. Unity displays the anatomy content relative to the target object configured in each scene. The original assets and settings were retained while the presentation layer was adapted.

The Android build environment uses JDK 8, Android SDK platform 28 and build-tools 28.0.3 for the legacy packaging route. The current package has minimum API 23, target API 28 and the ARMv7 architecture. These are properties of the classroom APK. They do not represent a current Play Store submission configuration or proof of compatibility with ARM64-only devices.

## 3.5 Development and Demonstration Hardware

The development setup was prepared on a Windows laptop with 24 GB RAM. The initial application check used a Tecno Spark Go 2023. For the demonstration, a laptop screen or a printed sheet provides the tracking picture, and the Android phone supplies the camera and display. A charging cable and a local copy of the APK are useful so that the demonstration does not depend on finding the download again at the venue.

# CHAPTER 4: SYSTEM DESIGN

## 4.1 Overall Workflow

The application begins with model selection. Selecting a button loads the corresponding anatomy scene. The user then points the camera at the supplied target picture. When the tracking system recognizes the reference, the scene's content can be displayed in relation to it. The user inspects the content, changes its presentation with the controls and returns to the menu to choose another structure.

This sequence separates the choice of content from the recognition of the picture. Choosing Heart determines which anatomy scene is loaded. It does not mean that a random photograph of a heart becomes the required target. The stored target configuration continues to define the picture that the application expects.

## 4.2 Scene Organisation

The opening scene is OpenScene. The model scenes are Skeleton, Skull, HumanBody, Heart and Brain. These names are included in the build configuration and are used by the navigation code. A scene name passed to SceneManager.LoadScene must correspond to a scene included in the built application.

Each anatomy scene contains the inherited camera and target arrangement, the relevant model content and supporting scene objects. The adaptation adds a common interface at startup. It replaces the original canvas presentation without removing the target or model objects. This approach keeps the original tracking arrangement while giving the application a consistent selection and inspection experience.

## 4.3 Parent and Child Transforms

The ImageTarget object supplies a parent reference for the anatomy content. A child object's local position, rotation and scale describe its relationship to that parent. Changes to the tracked reference can therefore affect the displayed placement without requiring the application to calculate every model vertex again.

A model's mesh and its Transform are different things. The mesh contains geometry. The Transform determines how an instance is placed and scaled in the scene. A material controls aspects of surface appearance. Understanding these roles helps explain why changing a scale value makes the displayed object larger without creating a more detailed anatomical mesh.

The reset function stores and restores local transforms of the selected model roots. It is a presentation reset. It is not a new tracking calibration and does not alter the target database. The size controls also operate on the model presentation rather than changing the physical dimensions of the printed target.

## 4.4 Camera and Model Rendering

The real camera view and the virtual camera work together in the AR experience. The tracking system processes observations of the configured image. Unity renders the model using its geometry, materials, lights and scene camera. The perceived alignment on the phone screen depends on the tracking reference and the content arrangement being used together.

The models are stored assets. They are not generated from the phone's current image. This explains both an advantage and a limitation of the design. The application can display prepared content without reconstructing it during the demonstration, but it can only show the content that has been included and configured.

## 4.5 Interface Design

The interface uses a dark background and a common accent color so that the model choices and controls are easy to distinguish. The app is named Anatomy AR. Viewer screens use the same neutral title rather than repeating a student's name. Team information and the original-project acknowledgment are placed in Credits.

The model screen has navigation at the top and an educational panel with inspection controls at the bottom. The central area is reserved for the camera and anatomy content. Help explains the target requirement and scanning steps. The design aims to keep technical build details out of the learner's normal path through the application.

## 4.6 Data Flow and Boundaries

The camera supplies image observations, Vuforia supplies the target reference, Unity draws the chosen model and the interface accepts user actions. Scene navigation changes which content is active. Size and rotation controls change its presentation. These operations are connected, but each has a separate responsibility.

Keeping these boundaries clear makes faults easier to investigate. A missing model may involve the selected scene or tracking conditions. A control that does not respond may involve interface input. An installation failure occurs before either of those runtime stages and must be investigated as a packaging or device-compatibility problem.

# CHAPTER 5: IMPLEMENTATION

## 5.1 Starting from the Existing Project

The base project was obtained from the AnatomyViewerAR repository [1]. It supplied the anatomy models, textures, materials, scenes, target database and original Vuforia integration. The original BSD 2-Clause license was retained, and the application's Credits acknowledge danMoksh and the original team. Reusing that work is stated directly in the report rather than presenting every asset as a new creation.

The adaptation concentrates on the user interface, educational descriptions, inspection controls, build preparation and submission material. The source is maintained in the AR_Anatomy repository. Generated Unity caches and local Android tools are kept outside the tracked source so that the repository remains understandable to a reviewer.

## 5.2 Creating the Common Interface

AnatomyUI.cs registers a scene-loaded callback for the opening scene and the five anatomy scenes. When one of those scenes loads, it creates an interface object. The opening screen displays the model choices, while the model screens display navigation, information and inspection controls. The same interface code is therefore reused across the anatomy scenes.

The UI is built from a Canvas, text elements, images and buttons. A CanvasScaler defines the reference layout. Button callbacks connect the visible controls to scene loading or a model operation. The EventSystem handles interface input. These are ordinary Unity UI components, so the interface logic can be inspected without changing the tracking engine.

The main menu uses readable model names even where the scene file has a compact name such as HumanBody. This is a small distinction, but it keeps development identifiers from becoming awkward interface labels. The help and credits panels open within the current scene and can be closed without reselecting the anatomy model.

## 5.3 Scene Navigation

The navigation code uses SceneManager.LoadScene. The selected button identifies the scene to load, and the build script includes the corresponding scene paths. Returning to Menu loads OpenScene. Consistency between the code names and build scene list is necessary; a correctly drawn button does not establish that its destination exists in the final package.

The legacy LoadGame script was updated to use SceneManager for its scene-loading call. This makes the navigation behavior explicit in the source. The application also handles the Android back action: a visible modal can close, and a model screen can return to the menu.

## 5.4 Model Size Controls

The smaller and larger buttons apply a multiplier to the original model-root scales. The multiplier is clamped between 0.3 and 3.0. Clamping prevents repeated button presses from shrinking the presentation indefinitely or making it arbitrarily large. The calculation changes the scale used for rendering; it does not change the mesh file or establish a physical measurement.

At scene startup, the interface records the model-root transforms needed by the controls. Each root has a corresponding initial position, rotation and scale. Keeping these values separate from the current values allows reset to restore a known starting presentation. The code checks whether a stored Transform still exists before using it.

## 5.5 Reset and Rotation

Reset sets the shared size multiplier back to one and restores the captured local transforms of the model roots. This gives the learner a convenient way to recover the starting view after using the inspection controls. It also gives the demonstrator a repeatable starting state when showing the same model more than once.

Automatic rotation is inherited through the Rotate script. Its Update method rotates the object around the Y-axis using Time.deltaTime. Multiplying the intended speed by elapsed frame time expresses the rotation per second rather than per rendered frame [3]. The pause/resume control enables or disables those Rotate components so that the user can stop the moving presentation for inspection.

## 5.6 Touch Input Guards

The inherited pinch-scaling script was adjusted to check that two touches and a selected Transform exist before performing a scale calculation. It records a starting finger distance and starting scale, then compares the current separation with that starting distance. A lower bound on the initial distance avoids an invalid division.

Touches over interface controls are excluded from this pinch operation. This matters because a phone screen is being used both for model interaction and for pressing buttons. Without an input guard, a gesture intended for the interface could also influence a model. The device acceptance test still needs to confirm the combined behavior on the presentation phone.

## 5.7 Resolving Build Problems

The original source contained an unused model-recognition sample handler whose API did not match the installed bundled Vuforia version. It caused compilation errors even though the anatomy application used image targets rather than that sample feature. The unused handler was removed and its editor attachment hook was adjusted for the image-target project.

The Android packaging step initially waited on a dependency used by the old Gradle route. The build was completed with Unity's internal Android packaging method and the installed Android tools. This was a build-environment decision for the legacy project, not a claim that the source had been migrated to a current Unity or Vuforia runtime.

## 5.8 Signing and Identifying the APK

AnatomyBuild.cs configures the application name, package identifier, scenes and Android settings. The final release uses the application identifier com.arvrlab.anatomyar and version 1.0.1. After packaging, Android signing tools sign and verify the distribution file. The build script checks the signing result rather than relying only on Unity's build-success message.

The signed package is distributed as AnatomyAR.apk. Its checksum is supplied with the release and recorded in the build verification file. A checksum identifies a particular file; it is useful when confirming which APK was tested or submitted. It does not establish that all runtime features have passed a device test.

# CHAPTER 6: OPERATION AND DEMONSTRATION

## 6.1 Preparing the Phone and Target

The phone requires the Anatomy AR application and permission to use its camera. The laptop or printed sheet provides the configured target picture. Before the viva, the demonstrator should keep a local copy of both the APK and the target, check the phone charge and confirm that the target can be displayed clearly without reflections.

The target should remain flat and its proportions should not be distorted. When it is shown on a laptop, the whole picture should be visible rather than cropped by a browser window. A printed copy offers another option if the screen introduces glare. The picture supplied in the Demo folder is the reference used by the project.

## 6.2 Installing and Opening the Application

The release page contains AnatomyAR.apk, the report and the checksum file. The APK can be downloaded to the phone and opened through its file manager. Installation follows the Android prompts available on that device. The application appears under the name Anatomy AR. Its package identifier is separate from the original senior application.

When the application opens, the menu presents Skeleton, Skull, Human body, Heart and Brain. The user selects one of these options and allows camera access if requested. If the application cannot open the camera, that issue must be resolved before attempting to judge target tracking.

## 6.3 Viewing a Model

The user points the camera at the full target picture and holds the phone steadily while the reference is acquired. Once the anatomy content is visible, the phone can be moved slowly to inspect it from other viewpoints. The object is rendered on the screen in relation to the target; it is not physically present above the paper or laptop.

The educational panel identifies the selected structure and gives a short description. Smaller and Larger adjust the model-root presentation. Reset restores the captured starting transforms. Pause rotation stops the automatic motion, and Resume rotation starts it again. Menu returns to model selection so that another structure can be demonstrated.

## 6.4 A Practical Viva Sequence

A clear demonstration begins with the problem being addressed: a learner may want to inspect anatomy from more than one fixed view. The demonstrator can then open the application, select Skull, scan the picture and show the resulting model. After that, the size and rotation controls can be demonstrated before returning to the menu and opening another structure.

The technical explanation should follow the same sequence. Unity manages the scenes and rendering. Vuforia recognizes and tracks the configured image. The target object provides a reference for the model. C# scripts connect the menu and controls to scene loading and Transform operations. This explanation is easier to assess when each concept is connected to something visible in the demonstration.

Both members should be prepared to repeat the complete workflow and explain their own actual contribution. The project is based on existing source, so the inherited content and the adaptation should be distinguished. A short backup recording is useful, but it does not replace the working demonstration required by the laboratory instructions.

## 6.5 Troubleshooting During Preparation

If no anatomy content appears, first confirm the selected scene, camera permission and target picture. Then check whether the whole target is visible and whether glare or blur makes it difficult to observe. Changing several development settings at once is less useful than checking these basic conditions in sequence.

An installation failure is a different type of problem. The exact Android message, phone model and installed operating-system version should be recorded. The legacy package contains ARMv7 libraries. A phone that accepts only ARM64 applications needs a different runtime build, so successful installation on the Tecno does not establish compatibility with every future Realme device.

# CHAPTER 7: VERIFICATION AND RESULTS

## 7.1 Verification Method

Verification was divided into source compilation, package inspection and device observation. Compilation checks whether the scripts and assets can be processed into an Android build. Package inspection checks properties of the resulting file. Device observation checks the installed application's behavior with a real camera and target. These stages provide different evidence and should not be treated as interchangeable.

The original APK was used for the initial phone check. The user reported that the full-body, head and skull views worked on the Tecno Spark Go 2023. This established a useful baseline for the inherited project on that phone. It did not automatically verify the later changes to the application.

## 7.2 Compilation and Packaging Result

The adapted project compiled and completed Android packaging successfully with Unity 2018.2.14f1. The resulting APK archive passed an integrity check. Package inspection identified the label Anatomy AR, version 1.0.1 and the identifier com.arvrlab.anatomyar. The package contains the ARMv7 native runtime and uses minimum API 23 and target API 28.

Android signature verification passed for both the v1 and v2 signature schemes. This check is important because an unsigned archive is not a valid final installation package merely because it has an .apk extension. The final distributed file is the signed AnatomyAR.apk supplied through GitHub Releases.

The release file contains the built application, model content and packaged tracking data. The build record and checksum provide a way to identify the exact version distributed for testing. These checks establish a usable build artifact and its expected metadata; they do not measure tracking stability or confirm every interaction on a phone.

## 7.3 Visual Inspection of the Project

The report includes previews captured from the actual Unity project. They show the implemented menu, anatomy assets, descriptions and control layout. The model previews were prepared in Unity for documentation and are labeled accordingly. They are not screenshots of successful phone-camera tracking.

This distinction allows the report to include useful visual output while keeping the evidence clear. A phone screenshot would show the camera background and the tracked content under the conditions of that device test. A Unity preview instead shows the stored scene content and interface arrangement. Both can be useful, but they answer different questions.

## 7.4 Acceptance Test for the Adapted APK

The remaining acceptance step is to install the signed adapted release on the Tecno and exercise the complete workflow. The test should record the device model, installed Android version and APK version. It should cover launch, camera permission, target acquisition, target loss and recovery, and selection of all five anatomy scenes.

The same session should check Menu, Help, Credits, Smaller, Larger, Reset and pause/resume rotation. Closing and reopening the application checks whether the starting workflow remains usable. A short screen recording and several screenshots should be retained as the record of the final demonstration build.

Realme compatibility remains untested. No frame-rate measurements, controlled lighting study or learning-outcome experiment was carried out as part of the recorded checks. The report therefore does not assign numerical accuracy, speed or educational-improvement values to the application.

## 7.5 Result Summary

The completed work provides a compiled and signed Anatomy AR release, organized source, a supplied target picture and a documented interface. The recorded phone success belongs to the original baseline application. Final runtime acceptance of the adapted APK is pending the presentation-device test. This is the boundary between the result already established and the check still needed before the viva.

## 7.6 Repeating the Package Checks

The package checks can be repeated when the APK is copied to another folder or downloaded for the demonstration. The Android build-tools command aapt dump badging AnatomyAR.apk reports the application label, package identifier and supported Android configuration. For this release, the expected label is Anatomy AR and the identifier is com.arvrlab.anatomyar. Reading these fields is more reliable than identifying an application by a similar file name.

The command apksigner verify --verbose AnatomyAR.apk checks the package signature. A successful result confirms that the signed archive passes the verification performed by that tool. It does not establish camera compatibility or successful target recognition. Those observations must come from running the application on the intended phone.

A SHA-256 checksum identifies the exact file. After downloading the release, its checksum can be compared with SHA256SUMS.txt. Matching values show that the downloaded bytes match the published build. If the values differ, the file should be downloaded again before the demonstration. The size of installed application storage is a separate value and may include extracted libraries and application data.

These checks also help distinguish the inherited baseline from the adapted application. Both may remain installed because their package identifiers differ. The demonstrator should open Anatomy AR and confirm its five-model menu before scanning the target. Keeping the tested APK and its checksum together prevents confusion when several earlier downloads are present.

# CHAPTER 9: DISCUSSION, LIMITATIONS AND FUTURE SCOPE

## 9.1 What the Project Demonstrates

The project connects several laboratory concepts in one visible workflow. An image target provides a physical reference. The tracking engine supplies its pose. Unity renders a stored model relative to that reference. Interface controls change the scene or the model presentation. The learner can connect these concepts to the application rather than treating them as unrelated definitions.

The adaptation also demonstrates the practical work required to prepare an existing project for presentation. Matching the editor, resolving an unused sample-script error, completing Android packaging and verifying signatures are part of delivering a project that can be reviewed. They are separate from designing the original tracking SDK or modelling every anatomy asset.

## 9.2 Limitations

The application depends on the configured target and on conditions that allow it to be observed. Glare, blur, poor lighting and partial visibility can interfere with the demonstration. The anatomy assets are simplified representations, and model scale is controlled for inspection rather than for measurement of a real structure.

The project uses a legacy runtime and ARMv7 libraries. Device support must therefore be checked instead of inferred from the Android brand or model name alone. The interface and controls also need final testing together with the camera workflow, since an editor preview cannot reproduce every aspect of touch input or camera behavior.

The educational descriptions are introductory. The project is not intended for diagnosis, surgery planning or patient advice. No study of learner performance was conducted, so the report treats improved engagement or learning as a possible direction for evaluation rather than as a measured result.

## 9.3 Future Development

A useful next step is migration to a supported editor and tracking SDK with an ARM64 build. That change should preserve the known target and model behavior while being validated on the intended devices. It should be treated as a migration project with its own tests, not as a version-number change that guarantees compatibility.

Further educational work could add carefully verified labels, a small quiz and more detailed descriptions of the visible structures. Accessibility improvements could include adjustable text size and clearer guidance when the target is not found. A structured user study could then compare the experience with a conventional diagram or 3D viewer.

## 9.4 Lessons from Implementation

Preparing the inherited project showed why editor compatibility matters. The anatomy scenes were not the only code considered during compilation: an unused tracking sample could also stop the build. Resolving that issue required identifying the code that the image-target workflow actually used and keeping the required tracking integration intact.

The installation workflow provided another practical lesson. Editing the Unity project changes its source, but it does not update an application already installed on a phone. A fresh build must be produced, signed, transferred and installed. Checking the application label and package identifier helps confirm which version is being opened, especially when the original and adapted applications coexist.

Packaging and runtime behavior need separate evidence. A successful editor build log was followed by checks of the final archive and Android signature. These checks made the package reviewable, while the camera and touch controls still require a device session. Keeping these stages distinct makes it easier to locate a failure and explain what has already been verified.

The target picture is also part of the demonstration, rather than an incidental illustration. Clear instructions about showing the complete supplied target are as necessary as the model-selection menu. During the viva, each student should connect this visible workflow with the underlying concepts: image recognition identifies the reference, tracking estimates its pose, rendering places the model, and interaction changes its presentation.

## 9.5 Conclusion

Anatomy AR provides a practical image-target anatomy viewer based on an acknowledged existing Unity and Vuforia project. The adaptation adds a common interface, educational descriptions, inspection controls and organized submission material. The Android build, archive inspection and signature checks were completed, and the source and release files were published in the project repository.

The project illustrates how recognition, tracking, rendering and interaction work together. Its final acceptance depends on testing the adapted APK on the presentation phone and keeping the resulting evidence with the report. Both students should be able to explain the workflow, identify the reused content and demonstrate the controls with an understanding of the application's limits.
