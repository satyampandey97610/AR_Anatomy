using UnityEngine;
using UnityEngine.EventSystems;

public class CSharpscaling : MonoBehaviour
{
    public float initialFingersDistance;
    public Vector3 initialScale;
    public static Transform ScaleTransform;
    bool pinching;
    Transform selected;

    void Update()
    {
        if (Input.touchCount != 2 || ScaleTransform == null)
        { pinching = false; return; }
        Touch first = Input.GetTouch(0), second = Input.GetTouch(1);
        if (EventSystem.current != null &&
            (EventSystem.current.IsPointerOverGameObject(first.fingerId) ||
             EventSystem.current.IsPointerOverGameObject(second.fingerId)))
        { pinching = false; return; }
        float distance = Vector2.Distance(first.position, second.position);
        if (!pinching || selected != ScaleTransform || first.phase == TouchPhase.Began || second.phase == TouchPhase.Began)
        {
            selected = ScaleTransform;
            initialFingersDistance = Mathf.Max(distance, 1f);
            initialScale = selected.localScale;
            pinching = true;
        }
        selected.localScale = initialScale * Mathf.Clamp(distance / initialFingersDistance, .3f, 3f);
    }
}
