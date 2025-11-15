using UnityEngine;
using System.Collections.Generic;

public class ObjectSpawner : MonoBehaviour
{
    public GameObject objectPrefab;
    public Transform player;
    public float spawnDistance = 50f;
    public float spawnInterval = 30f;
    public float minSpawnDistance = 10f;
    public float minDistanceFromPlayer = 10f;
    public Transform leftWall;
    public Transform rightWall;
    public float wallMargin = 1f; // Margin to prevent spawning inside the walls
    private float nextSpawnPositionZ = 0f;

    private List<Vector3> spawnedObstacles = new List<Vector3>();

    void Update()
    {
        if (player.position.z >= nextSpawnPositionZ)
        {
            SpawnObstacles();
            nextSpawnPositionZ += spawnInterval;
        }
    }

    void SpawnObstacles()
    {
        for (int i = 0; i < 1; i++)
        {
            Vector3 randomPosition;
            int attempts = 0;
            bool validPositionFound = false;

            do
            {
                randomPosition = new Vector3(
                    Random.Range(leftWall.position.x + wallMargin, rightWall.position.x - wallMargin), // Ensure X is between walls with margin
                    2.0f,
                    nextSpawnPositionZ + Random.Range(0, spawnInterval)
                );

                if (IsPositionValid(randomPosition) && IsFarEnoughFromPlayer(randomPosition))
                {
                    validPositionFound = true;
                }

                attempts++;
            }
            while (!validPositionFound && attempts < 20);

            if (validPositionFound)
            {
                Instantiate(objectPrefab, randomPosition, Quaternion.identity);
                spawnedObstacles.Add(randomPosition);
            }
        }
    }

    bool IsPositionValid(Vector3 newPosition)
    {
        foreach (Vector3 obstaclePosition in spawnedObstacles)
        {
            if (Vector3.Distance(newPosition, obstaclePosition) < minSpawnDistance)
            {
                return false;
            }
        }
        return true;
    }

    bool IsFarEnoughFromPlayer(Vector3 newPosition)
    {
        if (Vector3.Distance(new Vector3(newPosition.x, player.position.y, newPosition.z), player.position) < minDistanceFromPlayer)
        {
            return false;
        }

        if (newPosition.z <= player.position.z)
        {
            return false;
        }

        return true;
    }
}
