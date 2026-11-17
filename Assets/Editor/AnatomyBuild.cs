using System;
using System.IO;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;

public static class AnatomyBuild
{
    [MenuItem("Anatomy/Build Android APK")]
    public static void Android()
    {
        string directory = Path.GetFullPath(Path.Combine(Application.dataPath, "../../Builds"));
        Directory.CreateDirectory(directory);
        string sdk = Path.GetFullPath(Path.Combine(Application.dataPath, "../../AndroidSDK"));
        if (Directory.Exists(sdk)) EditorPrefs.SetString("AndroidSdkRoot", sdk);
        string jdk = Environment.GetEnvironmentVariable("ANATOMY_JDK_PATH");
        if (!String.IsNullOrEmpty(jdk)) EditorPrefs.SetString("JdkPath", jdk);
        EditorUserBuildSettings.androidBuildSystem = AndroidBuildSystem.Internal;
        PlayerSettings.companyName = "Satyam Pandey";
        PlayerSettings.productName = "Anatomy AR";
        PlayerSettings.SetApplicationIdentifier(BuildTargetGroup.Android, "com.arvrlab.anatomyar");
        PlayerSettings.bundleVersion = "1.0";
        PlayerSettings.Android.bundleVersionCode = 1;
        PlayerSettings.Android.minSdkVersion = (AndroidSdkVersions)23;
        PlayerSettings.Android.targetSdkVersion = (AndroidSdkVersions)28;
        PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARMv7;
        PlayerSettings.defaultInterfaceOrientation = UIOrientation.Portrait;
        PlayerSettings.SetScriptingBackend(BuildTargetGroup.Android, ScriptingImplementation.Mono2x);
        string[] scenes = { "OpenScene", "Skeleton", "Skull", "HumanBody", "Heart", "Brain" };
        for (int i = 0; i < scenes.Length; i++) scenes[i] = "Assets/Scenes/" + scenes[i] + ".unity";
        string apk = Path.Combine(directory, "AnatomyAR.apk");
        BuildReport report = BuildPipeline.BuildPlayer(scenes, apk, BuildTarget.Android, BuildOptions.None);
        if (report.summary.result != BuildResult.Succeeded) throw new Exception("Android build failed: " + report.summary.result);
        // The legacy internal packager may leave its output unsigned with current JDKs.
        // Verify the final distribution package rather than relying on the Unity success message.
        if (String.IsNullOrEmpty(jdk)) jdk = EditorPrefs.GetString("JdkPath");
        string java = Path.Combine(jdk, "bin/java.exe");
        string signer = Path.Combine(EditorPrefs.GetString("AndroidSdkRoot"), "build-tools/28.0.3/lib/apksigner.jar");
        string key = Path.Combine(Environment.GetEnvironmentVariable("USERPROFILE"), ".android/debug.keystore");
        if (!File.Exists(java) || !File.Exists(signer) || !File.Exists(key))
            throw new Exception("APK built but signing tools or the local development keystore are missing. Do not distribute unsigned output.");
        Run(java, "-jar " + Quote(signer) + " sign --ks " + Quote(key) + " --ks-key-alias androiddebugkey --ks-pass pass:android --key-pass pass:android " + Quote(apk));
        Run(java, "-jar " + Quote(signer) + " verify --verbose " + Quote(apk));
        Debug.Log("ANATOMY_BUILD_SUCCESS: " + directory);
    }

    static string Quote(string value) { return "\"" + value.Replace("\"", "") + "\""; }

    static void Run(string executable, string arguments)
    {
        var info = new System.Diagnostics.ProcessStartInfo(executable, arguments);
        info.UseShellExecute = false;
        info.CreateNoWindow = true;
        info.RedirectStandardOutput = true;
        info.RedirectStandardError = true;
        using (var process = System.Diagnostics.Process.Start(info))
        {
            string output = process.StandardOutput.ReadToEnd();
            string errors = process.StandardError.ReadToEnd();
            process.WaitForExit();
            if (process.ExitCode != 0) throw new Exception("APK signing/verification failed: " + errors);
            Debug.Log(output);
        }
    }
}
