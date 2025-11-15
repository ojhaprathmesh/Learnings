using UnityEngine;

public class FollowPlayer : MonoBehaviour
{
    public Transform target;
    public Vector3 offset;
    private bool firstPerson = false;

    void Update() {
        if (Input.GetKeyDown(KeyCode.V)) {
            firstPerson = !firstPerson; // Toggle the firstPerson view
        }
    }

    void LateUpdate() {
        if (firstPerson) {
            transform.SetPositionAndRotation(target.position, target.rotation);
        } else {
            transform.position = target.position + offset;
            transform.LookAt(target);
        }
    }
}
