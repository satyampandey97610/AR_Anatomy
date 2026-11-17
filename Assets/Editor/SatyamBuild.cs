using System;
using System.IO;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;

public static class SatyamBuild
{
    [MenuItem("Satyam/Build Android APK")]
    public static void Android()
    {
        string directory = Path.GetFullPath(Path.Combine(Application.dataPath, "../../Builds"));
        Directory.CreateDirectory(directory);
        string sdk = Path.GetFullPath(Path.Combine(Application.dataPath, "../../AndroidSDK"));
        if (Directory.Exists(sdk)) EditorPrefs.SetString("AndroidSdkRoot", sdk);
        string jdk = Environment.GetEnvironmentVariable("SATYAM_JDK_PATH");
        if (!String.IsNullOrEmpty(jdk)) EditorPrefs.SetString("JdkPath", jdk);
        EditorUserBuildSettings.androidBuildSystem = AndroidBuildSystem.Gradle;
        PlayerSettings.companyName = "Satyam Pandey";
        PlayerSettings.productName = "Satyam Anatomy AR";
        PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.Android, "com.satyampandey.anatomyar");
        PlayerSettings.bundleVersion = "1.0";
        PlayerSettings.Android.bundleVersionCode = 1;
        PlayerSettings.Android.minSdkVersion = (AndroidSdkVersions)23;
        PlayerSettings.Android.targetSdkVersion = (AndroidSdkVersions)28;
        PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARMv7;
        PlayerSettings.defaultInterfaceOrientation = UIOrientation.Portrait;
        PlayerSettings.SetScriptingBackend(BuildTargetGroup.Android, ScriptingImplementation.Mono2x);
        string[] scenes = { "OpenScene", "Skeleton", "Skull", "HumanBody", "Heart", "Brain" };
        for (int i = 0; i < scenes.Length; i++) scenes[i] = "Assets/Scenes/" + scenes[i] + ".unity";
        BuildReport report = BuildPipeline.BuildPlayer(scenes, Path.Combine(directory, "SatyamAnatomyAR-Tecno.apk"), BuildTarget.Android, BuildOptions.None);
        if (report.summary.result != BuildResult.Succeeded) throw new Exception("Android build failed: " + report.summary.result);
        Debug.Log("SATYAM_BUILD_SUCCESS: " + directory);
    }
}
