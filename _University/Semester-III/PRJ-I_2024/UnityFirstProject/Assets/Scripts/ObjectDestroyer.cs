using UnityEngine;
using System.Collections;

public class ObstacleDestroyer : MonoBehaviour
{
    public Transform player;
    public float despawnDelay = 2f; // Delay before despawning

    void Update()
    {
        DestroyObstaclesBehindPlayer();
    }

    void DestroyObstaclesBehindPlayer()
    {
        // Find all objects with the "Obstacle" tag in the scene
        GameObject[] obstacles = GameObject.FindGameObjectsWithTag("Obstacle");

        foreach (GameObject obstacle in obstacles)
        {
            // Check if the obstacle's z position is less than the player's z position
            if (obstacle.transform.position.z < player.position.z)
            {
                StartCoroutine(DestroyAfterDelay(obstacle));
            }
        }
    }

    IEnumerator DestroyAfterDelay(GameObject obstacle)
    {
        yield return new WaitForSeconds(despawnDelay); // Wait for 2 seconds
        Destroy(obstacle); // Destroy the obstacle after the delay
    }
}
