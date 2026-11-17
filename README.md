# Satyam Anatomy AR

An educational Android image-target AR viewer adapted from [AnatomyViewerAR](https://github.com/danMoksh/AnatomyViewerAR).

## Team
- Satyam Pandey ? 0901AI231059
- Kartikey Tiwari ? 0901AI231033

## Changes in this adaptation
- New Satyam menu and consistent anatomy navigation.
- Educational descriptions of five anatomy models.
- Bounded size controls and model transform reset.
- Pause/resume automatic rotation.
- In-app instructions and original project credits/license.
- Separate Android application ID: `com.satyampandey.anatomyar`.

## Build
Original editor: Unity 2018.2.14f1 with Android and bundled Vuforia support.
Open the project, resolve the Unity license and Android tool paths, then use **Satyam > Build Android APK**.
The build script outputs `../Builds/SatyamAnatomyAR-Tecno.apk`.
This legacy build is ARMv7, target SDK 28, minimum SDK 23. It is NOT an ARM64 build and cannot be claimed compatible with all newer phones. A Realme device test is required; ARM64-only devices require a newer runtime/SDK migration.

## Demo
Display `../Phone Demo/TARGET-PICTURE.png` on a laptop or print it. Select a model and scan the full picture with the app. This app displays stored models; it does not reconstruct arbitrary photos.

## Status
The upstream APK was reported working by the user on a Tecno Spark Go 2023. The adapted source must be compiled and device-tested before submission. Do not use upstream results as test results for this adaptation.

## Attribution
Original project: danMoksh. Original team: Moksh Dandotiya, Yuvraj Tiwari, Mohit Sahu. Original BSD 2-Clause license retained in LICENSE and in-app Credits.
Model and other third-party asset rights remain subject to their respective licenses.
