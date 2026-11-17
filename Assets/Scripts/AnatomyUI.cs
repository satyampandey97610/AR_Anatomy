using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

// Presentation and learning controls added to the original image-target project.
public class AnatomyUI : MonoBehaviour
{
    static readonly string[] Scenes = { "Skeleton", "Skull", "HumanBody", "Heart", "Brain" };
    static readonly string[] Names = { "Skeleton", "Skull", "Human body", "Heart", "Brain" };
    static readonly string[] Facts = {
        "SKELETON\nThe skeleton supports the body, protects organs and works with muscles to enable movement.",
        "SKULL\nThe skull protects the brain and forms the framework of the face.",
        "HUMAN BODY\nOrgans and body systems work together to keep the body functioning.",
        "HEART\nThe heart pumps blood through the lungs and the rest of the body. It has four chambers.",
        "BRAIN\nThe brain coordinates movement, processes sensory information and supports memory and thought."
    };
    readonly List<Transform> roots = new List<Transform>();
    readonly List<Vector3> positions = new List<Vector3>();
    readonly List<Quaternion> rotations = new List<Quaternion>();
    readonly List<Vector3> scales = new List<Vector3>();
    Canvas canvas;
    GameObject modal;
    Font font;
    float size = 1f;
    bool spinning = true;
    Text rotationLabel;
    static readonly Color Ink = new Color(.055f, .10f, .17f);
    static readonly Color Accent = new Color(.02f, .64f, .60f);

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.BeforeSceneLoad)]
    static void Register()
    {
        SceneManager.sceneLoaded -= OnScene;
        SceneManager.sceneLoaded += OnScene;
    }

    static void OnScene(Scene scene, LoadSceneMode mode)
    {
        if (System.Array.IndexOf(Scenes, scene.name) < 0 && scene.name != "OpenScene") return;
        new GameObject("Anatomy Interface").AddComponent<AnatomyUI>();
    }

    void Start()
    {
        font = Resources.GetBuiltinResource<Font>("Arial.ttf");
        // Replace legacy interface only. ARCamera, targets and models remain active.
        foreach (Canvas old in FindObjectsOfType<Canvas>()) old.gameObject.SetActive(false);
        GameObject go = new GameObject("Anatomy Canvas", typeof(RectTransform), typeof(Canvas), typeof(CanvasScaler), typeof(GraphicRaycaster));
        go.transform.SetParent(transform, false);
        canvas = go.GetComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.sortingOrder = 100;
        CanvasScaler scaler = go.GetComponent<CanvasScaler>();
        scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(720, 1280);
        scaler.matchWidthOrHeight = .5f;
        if (FindObjectOfType<UnityEngine.EventSystems.EventSystem>() == null)
            new GameObject("EventSystem", typeof(UnityEngine.EventSystems.EventSystem), typeof(UnityEngine.EventSystems.StandaloneInputModule));
        if (SceneManager.GetActiveScene().name == "OpenScene") Menu(); else Viewer();
    }

    RectTransform Box(string name, Transform parent, float x, float y, float w, float h)
    {
        RectTransform r = new GameObject(name, typeof(RectTransform)).GetComponent<RectTransform>();
        r.SetParent(parent, false);
        r.anchorMin = r.anchorMax = new Vector2(.5f, 1f);
        r.pivot = new Vector2(.5f, 1f);
        r.anchoredPosition = new Vector2(x, -y);
        r.sizeDelta = new Vector2(w, h);
        return r;
    }

    Text Label(Transform parent, string value, float x, float y, float w, float h, int pts, Color color)
    {
        Text t = Box("Text", parent, x, y, w, h).gameObject.AddComponent<Text>();
        t.text = value; t.font = font; t.fontSize = pts; t.color = color;
        t.alignment = TextAnchor.MiddleCenter; t.raycastTarget = false;
        return t;
    }

    RectTransform Panel(Transform parent, float x, float y, float w, float h, Color color)
    {
        RectTransform r = Box("Panel", parent, x, y, w, h);
        r.gameObject.AddComponent<Image>().color = color;
        return r;
    }

    Button Action(Transform parent, string title, float x, float y, float w, float h, UnityEngine.Events.UnityAction callback)
    {
        RectTransform r = Panel(parent, x, y, w, h, Accent);
        Button b = r.gameObject.AddComponent<Button>();
        b.targetGraphic = r.GetComponent<Image>();
        b.onClick.AddListener(callback);
        Label(r, title, 0, 0, w - 12, h, 25, Color.white);
        return b;
    }

    void Menu()
    {
        RectTransform bg = Panel(canvas.transform, 0, 0, 5000, 5000, Ink);
        bg.SetAsFirstSibling();
        Label(canvas.transform, "Anatomy AR", 0, 95, 660, 70, 42, Color.white);
        Label(canvas.transform, "Explore. Inspect. Learn.", 0, 170, 660, 60, 30, new Color(.3f, .91f, .81f));
        Label(canvas.transform, "Explore the human body in augmented reality", 0, 245, 640, 80, 25, Color.white);
        for (int i = 0; i < Scenes.Length; i++)
        {
            int selected = i;
            Action(canvas.transform, Names[i], 0, 365 + i * 112, 580, 86, () => SceneManager.LoadScene(Scenes[selected]));
        }
        Action(canvas.transform, "How to use", -153, 965, 274, 70, Help);
        Action(canvas.transform, "Credits", 153, 965, 274, 70, Credits);
        Label(canvas.transform, "AR/VR Lab Project\nImage-target anatomy learning", 0, 1085, 640, 90, 23, Color.white);
        Label(canvas.transform, "Educational visualization only", 0, 1190, 640, 40, 20, new Color(.7f, .76f, .83f));
    }

    void Viewer()
    {
        Panel(canvas.transform, 0, 0, 5000, 168, Ink);
        Label(canvas.transform, "ANATOMY AR", 0, 22, 680, 48, 28, Color.white);
        Action(canvas.transform, "Menu", -230, 88, 190, 60, () => SceneManager.LoadScene("OpenScene"));
        Action(canvas.transform, "Help", 0, 88, 190, 60, Help);
        Action(canvas.transform, "Credits", 230, 88, 190, 60, Credits);
        int index = System.Array.IndexOf(Scenes, SceneManager.GetActiveScene().name);
        RectTransform footer = Panel(canvas.transform, 0, 0, 720, 260, new Color(.055f, .10f, .17f, .95f));
        footer.anchorMin = footer.anchorMax = new Vector2(.5f, 0);
        footer.pivot = new Vector2(.5f, 0);
        footer.anchoredPosition = Vector2.zero;
        Label(footer, Facts[index], 0, 14, 660, 100, 25, Color.white);
        Action(footer, "Smaller", -226, 127, 200, 60, () => Resize(.8f));
        Action(footer, "Reset", 0, 127, 200, 60, ResetModel);
        Action(footer, "Larger", 226, 127, 200, 60, () => Resize(1.25f));
        Button spin = Action(footer, "Pause rotation", 0, 200, 400, 48, ToggleRotation);
        rotationLabel = spin.GetComponentInChildren<Text>();
        StartCoroutine(CaptureModels());
    }

    IEnumerator CaptureModels()
    {
        yield return null;
        GameObject target = GameObject.Find("ImageTarget");
        if (target == null) yield break;
        foreach (Transform child in target.transform)
        {
            if (child.name.StartsWith("ImageTargetMesh") || child.GetComponentInChildren<Renderer>(true) == null) continue;
            roots.Add(child); positions.Add(child.localPosition); rotations.Add(child.localRotation); scales.Add(child.localScale);
        }
    }

    void Resize(float factor)
    {
        size = Mathf.Clamp(size * factor, .3f, 3f);
        for (int i = 0; i < roots.Count; i++) if (roots[i]) roots[i].localScale = scales[i] * size;
    }

    void ResetModel()
    {
        size = 1f;
        for (int i = 0; i < roots.Count; i++) if (roots[i])
        { roots[i].localPosition = positions[i]; roots[i].localRotation = rotations[i]; roots[i].localScale = scales[i]; }
    }

    void ToggleRotation()
    {
        spinning = !spinning;
        foreach (Rotate component in FindObjectsOfType<Rotate>()) component.enabled = spinning;
        rotationLabel.text = spinning ? "Pause rotation" : "Resume rotation";
    }

    void Show(string title, string body)
    {
        if (modal) Destroy(modal);
        RectTransform shade = Panel(canvas.transform, 0, 0, 5000, 5000, new Color(0, 0, 0, .8f));
        modal = shade.gameObject;
        // A centered card uses its own top-anchored coordinate space.
        RectTransform card = Panel(shade, 0, 240, 660, 830, Ink);
        Label(card, title, 0, 24, 610, 70, 32, Color.white);
        Text text = Label(card, body, 0, 110, 590, 600, 23, Color.white);
        text.alignment = TextAnchor.UpperLeft;
        text.resizeTextForBestFit = true; text.resizeTextMinSize = 14; text.resizeTextMaxSize = 23;
        Action(card, "Close", 0, 735, 540, 64, () => Destroy(modal));
    }

    void Help()
    {
        Show("YOUR FIRST AR SCAN", "1. Display the supplied target picture on a laptop or print it.\n\n2. Choose a body part from the menu.\n\n3. Allow camera access and point your phone at the whole target picture.\n\n4. Move your phone slowly to inspect the model.\n\nUse Smaller, Larger and Reset to adjust it.\n\nUse even lighting and avoid reflections. The app recognizes its supplied target; it does not convert arbitrary photos into 3D models.");
    }

    void Credits()
    {
        TextAsset license = Resources.Load<TextAsset>("OriginalLicense");
        Show("ABOUT & CREDITS", "Anatomy AR\nAdaptation and interface: Satyam Pandey (0901AI231059).\nBatch member: Kartikey Tiwari (0901AI231033).\n\nBased on AnatomyViewerAR by danMoksh. Original team: Moksh Dandotiya, Yuvraj Tiwari and Mohit Sahu.\nUnity + Vuforia. Educational use; not a diagnostic tool.\n\n" + (license ? license.text : "See the original BSD 2-Clause LICENSE distributed with the project."));
    }

    void Update()
    {
        if (!Input.GetKeyDown(KeyCode.Escape)) return;
        if (modal) Destroy(modal);
        else if (SceneManager.GetActiveScene().name != "OpenScene") SceneManager.LoadScene("OpenScene");
        else Application.Quit();
    }
}
