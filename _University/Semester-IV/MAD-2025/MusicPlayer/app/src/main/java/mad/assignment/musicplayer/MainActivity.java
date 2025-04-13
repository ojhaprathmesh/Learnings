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
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private TextView songTitle;
    private ToggleButton playPauseToggle;
    private MediaPlayer mediaPlayer;
    private Uri selectedSong;
    private String songName;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button selectBtn = findViewById(R.id.selectBtn);
        playPauseToggle = findViewById(R.id.playPauseToggle);
        Button stopBtn = findViewById(R.id.stopBtn);
        songTitle = findViewById(R.id.songTitle);

        playPauseToggle.setEnabled(false); // disable until song is picked

        // Song picker
        ActivityResultLauncher<Intent> songPicker = registerForActivityResult(
                new ActivityResultContracts.StartActivityForResult(),
                result -> {
                    if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                        selectedSong = result.getData().getData();
                        songName = getFileName(selectedSong);
                        songTitle.setText("Now selected: " + songName);
                        playPauseToggle.setEnabled(true);
                        releasePlayer();
                    }
                }
        );

        selectBtn.setOnClickListener(v -> {
            Intent pickIntent = new Intent(Intent.ACTION_GET_CONTENT);
            pickIntent.setType("audio/*");
            songPicker.launch(Intent.createChooser(pickIntent, "Choose your track"));
        });

        playPauseToggle.setOnCheckedChangeListener((button, isChecked) -> {
            if (selectedSong == null) {
                Toast.makeText(this, "Please select a song first!", Toast.LENGTH_SHORT).show();
                playPauseToggle.setChecked(false);
                return;
            }

            if (mediaPlayer == null) {
                mediaPlayer = MediaPlayer.create(this, selectedSong);
                mediaPlayer.setOnCompletionListener(mp -> playPauseToggle.setChecked(false));
            }

            if (isChecked) {
                mediaPlayer.start();
                songTitle.setText("Playing: " + songName);
            } else if (mediaPlayer.isPlaying()) {
                mediaPlayer.pause();
                songTitle.setText("Paused: " + songName);
            }
        });

        stopBtn.setOnClickListener(v -> releasePlayer());
    }

    private String getFileName(Uri uri) {
        try (Cursor cursor = getContentResolver().query(uri, null, null, null, null)) {
            if (cursor != null && cursor.moveToFirst()) {
                int nameIndex = cursor.getColumnIndex(OpenableColumns.DISPLAY_NAME);
                if (nameIndex >= 0) return cursor.getString(nameIndex);
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
        songTitle.setText("Stopped: " + (songName != null ? songName : ""));
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        releasePlayer();
}
}