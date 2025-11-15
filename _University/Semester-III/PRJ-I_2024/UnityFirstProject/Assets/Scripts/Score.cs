using TMPro;
using UnityEngine;

public class Score : MonoBehaviour
{
    public Transform player;
    public TextMeshProUGUI scoreText;
    public bool isGameOver = false;

    void Update()
    {
        if (isGameOver) {
            scoreText.text = "Game Over";
        } else {
            scoreText.text = ((int)(player.position.z)/50).ToString("0");
        }
    }
}
