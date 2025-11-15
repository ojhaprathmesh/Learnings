using UnityEngine;

public class PlayerDivision : MonoBehaviour
{
    public GameObject cubePrefab;
    public int cubeCount = 4;
    public float cubeSize = 0.25f;
    public float disappearDelay = 2f;

    private bool isDivided = false;

    void OnCollisionEnter(Collision collision)
    {
        if (!isDivided && (collision.collider.CompareTag("Obstacle") || collision.collider.CompareTag("Wall")))
        {
            DivideIntoCubes(); // Split the player into cubes
        }
    }

    void DivideIntoCubes()
    {
        float startX = transform.position.x - (cubeSize * (cubeCount - 1)) / 2;
        float startY = transform.position.y - (cubeSize * (cubeCount - 1)) / 2;
        float startZ = transform.position.z - (cubeSize * (cubeCount - 1)) / 2;

        for (int x = 0; x < cubeCount; x++)
        {
            for (int y = 0; y < cubeCount; y++)
            {
                for (int z = 0; z < cubeCount; z++)
                {
                    Vector3 cubePosition = new(
                        startX + x * cubeSize,
                        startY + y * cubeSize,
                        startZ + z * cubeSize
                    );

                    GameObject cube = Instantiate(cubePrefab, cubePosition, Quaternion.identity);

                    // Set the tag to "CubeParticle"
                    cube.tag = "CubeParticle";

                    // Ensure the cube has a Rigidbody component
                    if (!cube.TryGetComponent<Rigidbody>(out var rb))
                    {
                        rb = cube.AddComponent<Rigidbody>();
                    }

                    rb.mass = 0.1f;
                }
            }
        }

        gameObject.SetActive(false); // Deactivate the original player object
        isDivided = true; // Mark as divided to prevent further divisions
    }
}
