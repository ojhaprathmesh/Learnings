using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public Rigidbody player;
    public float forwardForce;
    public float sidewaysForce;
    private bool moveRight, moveLeft;

    void Update()
    {
        moveRight = Input.GetKey(KeyCode.D);
        moveLeft = Input.GetKey(KeyCode.A);
    }

    // Used for physics calculation
    void FixedUpdate()
    {
        player.AddForce(0, 0, forwardForce * Time.deltaTime);

        if (moveRight)
        {
            player.AddForce(sidewaysForce * Time.deltaTime, 0, 0, ForceMode.VelocityChange);
        }

        if (moveLeft)
        {
            player.AddForce(-sidewaysForce * Time.deltaTime, 0, 0, ForceMode.VelocityChange);
        }
    }
}
