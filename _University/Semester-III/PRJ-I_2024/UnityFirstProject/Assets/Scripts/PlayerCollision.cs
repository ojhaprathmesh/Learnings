using UnityEngine;

public class PlayerCollision : MonoBehaviour {
    public PlayerMovement playerMovement;
    public Score score; // Reference to the Score script

    void OnCollisionEnter(Collision collisionInfo) {
        if (collisionInfo.collider.CompareTag("Obstacle") || collisionInfo.collider.CompareTag("Wall")) {
            playerMovement.enabled = false;
            
            // Disable all obstacle movements
            ObstacleMovementScript[] obstacles = FindObjectsOfType<ObstacleMovementScript>();
            foreach (ObstacleMovementScript obstacle in obstacles) {
                obstacle.enabled = false;
            }

            // Set the game over flag in the Score script
            score.isGameOver = true;
        }
    }
}
