package mad.assignment.musicplayer;

import android.content.Intent;
import android.database.Cursor;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Bundle;
import android.provider.OpenableColumns;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ToggleButton;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private TextView songTitle;
    private ToggleButton playPauseToggle;
    private MediaPlayer mediaPlayer;
    private Uri selectedSong;
    private String songName = "No song selected";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        songTitle = findViewById(R.id.songTitle);
        playPauseToggle = findViewById(R.id.playPauseToggle);
        Button selectBtn = findViewById(R.id.selectBtn);
        Button stopBtn = findViewById(R.id.stopBtn);

        playPauseToggle.setEnabled(false);

        ActivityResultLauncher<Intent> songPicker = registerForActivityResult(
            new ActivityResultContracts.StartActivityForResult(),
                result -> {
                if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                    selectedSong = result.getData().getData();
                    songName = getFileName(selectedSong);
                    songTitle.setText("Selected: " + songName);
                    playPauseToggle.setEnabled(true);
                    releasePlayer();
                }
            });

        selectBtn.setOnClickListener(v -> {
            Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
            intent.setType("audio/*");
            songPicker.launch(Intent.createChooser(intent, "Select a song"));
        });

        playPauseToggle.setOnCheckedChangeListener((btn, isPlaying) -> {
            if (selectedSong == null) {
                Toast.makeText(this, "Select a song first", Toast.LENGTH_SHORT).show();
                playPauseToggle.setChecked(false);
                return;
            }

            if (mediaPlayer == null) {
                mediaPlayer = MediaPlayer.create(this, selectedSong);
                mediaPlayer.setOnCompletionListener(mp -> playPauseToggle.setChecked(false));
            }

            if (isPlaying) {
                mediaPlayer.start();
                songTitle.setText("Playing: " + songName);
            } else {
                mediaPlayer.pause();
                songTitle.setText("Paused: " + songName);
            }
        });

        stopBtn.setOnClickListener(v -> {
            releasePlayer();
            songTitle.setText("Stopped: " + songName);
        });
    }

    private String getFileName(Uri uri) {
        try (Cursor cursor = getContentResolver().query(uri, null, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) {
                int nameIndex = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                return nameIndex >= 0 ? cursor.getString(nameIndex) : "Unknown";
            }
        }
        return "Unknown";
    }

    private void releasePlayer() {
        if (mediaPlayer != null) {
            if (mediaPlayer.isPlaying()) mediaPlayer.stop();
            mediaPlayer.release();
            mediaPlayer = null;
        }
        playPauseToggle.setChecked(false);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        releasePlayer();
    }
}
