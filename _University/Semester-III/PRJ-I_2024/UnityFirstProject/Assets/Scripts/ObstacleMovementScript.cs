using UnityEngine;

public class ObstacleMovementScript : MonoBehaviour {
    public float speed = 2f; // Speed of the oscillation
    public float minX = -5f; // Minimum X position (left wall)
    public float maxX = 5f;  // Maximum X position (right wall)
    private float direction = 1f; // 1 for moving right, -1 for moving left

    void Start() {
        // Randomize the initial position between the two walls
        float randomX = Random.Range(minX, maxX);
        transform.position = new Vector3(randomX, transform.position.y, transform.position.z);
        direction = Random.Range(0, 2) == 0 ? -1f : 1f;
    }

    void FixedUpdate() {
        MoveObstacle();
    }

    private void MoveObstacle() {
        transform.position += direction * speed * Time.deltaTime * Vector3.right;
    }

    private void OnCollisionEnter(Collision collisionInfo) {
        if (collisionInfo.gameObject.CompareTag("Wall") ||
            collisionInfo.gameObject.CompareTag("Obstacle")) {
            direction *= -1;
        }
    }
}
