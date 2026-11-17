using System;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

// Captures clearly labeled Unity previews, not simulated evidence of phone tracking.
[InitializeOnLoad]
public static class ReportPreview
{
    const string Active = "Anatomy.ReportPreview.Active";
    const string Index = "Anatomy.ReportPreview.Index";
    static readonly string[] Scenes = { "OpenScene", "Skeleton", "Skull", "HumanBody", "Heart", "Brain" };
    static double next;

    static ReportPreview() { EditorApplication.update += Tick; }

    [MenuItem("Anatomy/Capture report previews")]
    public static void Begin()
    {
        EditorPrefs.SetBool(Active, false);
        for (int i = 0; i < Scenes.Length; i++)
        {
            EditorSceneManager.OpenScene("Assets/Scenes/" + Scenes[i] + ".unity");
            var ui = new GameObject("Report preview interface").AddComponent<AnatomyUI>();
            ui.SendMessage("Start");
            Capture(Scenes[i], i > 0);
        }
        EditorApplication.Exit(0);
    }

    static void Tick()
    {
        if (!EditorPrefs.GetBool(Active, false)) { next = 0; return; }
        if (!EditorApplication.isPlaying)
        {
            if (!EditorApplication.isPlayingOrWillChangePlaymode) EditorApplication.isPlaying = true;
            next = 0;
            return;
        }
        if (next == 0) next = EditorApplication.timeSinceStartup + 4;
        if (EditorApplication.timeSinceStartup < next) return;
        int index = EditorPrefs.GetInt(Index, 0);
        try { Capture(Scenes[index], index > 0); }
        catch (Exception e) { UnityEngine.Debug.LogException(e); }
        index++;
        EditorPrefs.SetInt(Index, index);
        if (index >= Scenes.Length)
        {
            EditorPrefs.SetBool(Active, false);
            EditorApplication.isPlaying = false;
            EditorApplication.delayCall += () => EditorApplication.Exit(0);
        }
        else
        {
            SceneManager.LoadScene(Scenes[index]);
            next = EditorApplication.timeSinceStartup + 4;
        }
    }

    static void Capture(string name, bool model)
    {
        Camera camera = Camera.main ? Camera.main : UnityEngine.Object.FindObjectOfType<Camera>();
        if (!camera) throw new Exception("No camera in preview scene " + name);
        foreach (Behaviour b in camera.GetComponents<Behaviour>())
            if (b.GetType().Namespace == "Vuforia") b.enabled = false;
        camera.clearFlags = CameraClearFlags.SolidColor;
        camera.backgroundColor = new Color(.07f, .12f, .19f);
        camera.fieldOfView = 40;
        camera.nearClipPlane = .01f;
        camera.farClipPlane = 10000;
        camera.aspect = 720f / 1280f;
        if (model)
        {
            GameObject target = GameObject.Find("ImageTarget");
            bool found = false;
            Bounds bounds = new Bounds();
            if (target) foreach (Renderer renderer in target.GetComponentsInChildren<Renderer>(true))
            {
                if (renderer.name.StartsWith("ImageTargetMesh")) { renderer.enabled = false; continue; }
                Transform ancestor = renderer.transform;
                while (ancestor != target.transform && ancestor != null) { ancestor.gameObject.SetActive(true); ancestor = ancestor.parent; }
                renderer.enabled = true;
                if (!found) { bounds = renderer.bounds; found = true; } else bounds.Encapsulate(renderer.bounds);
            }
            if (found)
            {
                float tangent = Mathf.Tan(20 * Mathf.Deg2Rad);
                float distance = Mathf.Max(bounds.extents.y / (tangent * .55f), bounds.extents.x / (tangent * camera.aspect * .8f)) + bounds.extents.z;
                camera.transform.position = bounds.center + new Vector3(0, 0, -Mathf.Max(distance, .5f));
                camera.transform.LookAt(bounds.center);
            }
        }
        RenderTexture render = new RenderTexture(720, 1280, 24);
        render.Create();
        camera.targetTexture = render;
        foreach (Canvas canvas in UnityEngine.Object.FindObjectsOfType<Canvas>())
        {
            canvas.renderMode = RenderMode.WorldSpace;
            canvas.worldCamera = camera;
            canvas.planeDistance = 1f;
            var scaler = canvas.GetComponent<UnityEngine.UI.CanvasScaler>();
            if (scaler) scaler.enabled = false;
            canvas.scaleFactor = 1f;
            RectTransform rect = canvas.GetComponent<RectTransform>();
            rect.sizeDelta = new Vector2(720, 1280);
            rect.pivot = new Vector2(.5f, .5f);
            rect.position = camera.transform.position + camera.transform.forward;
            rect.rotation = camera.transform.rotation;
            rect.localScale = Vector3.one * (2f * Mathf.Tan(20f * Mathf.Deg2Rad) / 1280f);
        }
        Canvas.ForceUpdateCanvases();
        foreach (var graphic in UnityEngine.Object.FindObjectsOfType<UnityEngine.UI.Graphic>())
        {
            graphic.SetAllDirty();
            graphic.Rebuild(UnityEngine.UI.CanvasUpdate.PreRender);
        }
        camera.Render();
        RenderTexture.active = render;
        Texture2D picture = new Texture2D(720, 1280, TextureFormat.RGB24, false);
        picture.ReadPixels(new Rect(0, 0, 720, 1280), 0, 0);
        picture.Apply();
        string directory = Path.GetFullPath(Path.Combine(Application.dataPath, "../Documentation/Output"));
        Directory.CreateDirectory(directory);
        File.WriteAllBytes(Path.Combine(directory, name + "-UnityPreview.png"), picture.EncodeToPNG());
        camera.targetTexture = null;
        RenderTexture.active = null;
        UnityEngine.Object.DestroyImmediate(picture);
        UnityEngine.Object.DestroyImmediate(render);
        UnityEngine.Debug.Log("REPORT_PREVIEW_SAVED: " + name);
    }
}
