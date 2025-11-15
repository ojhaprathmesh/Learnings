using UnityEngine;

public class DestroyWhenStopped : MonoBehaviour
{
    public float stopThreshold = 0.1f;  // The velocity threshold to consider the object as "stopped"
    public float stopDuration = 2f;     // The time in seconds the object must be stopped before being destroyed

    private Rigidbody rb;
    private float stoppedTime = 0f;     // Time the object has been stopped

    private void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    private void Update()
    {
        if (rb != null && rb.velocity.magnitude <= stopThreshold)
        {
            stoppedTime += Time.deltaTime;  // Increment time if the object is stopped

            if (stoppedTime >= stopDuration)
            {
                Destroy(gameObject);        // Destroy the object after it has been stopped for more than stopDuration seconds
            }
        }
        else
        {
            stoppedTime = 0f;               // Reset the timer if the object starts moving again
        }
    }
}
