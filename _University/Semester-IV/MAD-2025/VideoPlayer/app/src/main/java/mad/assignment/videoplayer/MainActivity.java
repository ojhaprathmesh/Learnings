package mad.assignment.videoplayer;

import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.OpenableColumns;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.TextView;
import android.widget.ToggleButton;
import android.widget.VideoView;
import android.widget.MediaController;
import android.widget.Toast;

import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private VideoView videoView;
    private TextView videoTitle;
    private ToggleButton playPauseToggle;
    private Uri selectedVideo;
    private String videoName;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Make activity fullscreen
        getWindow().setFlags(
                WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN
        );
        setContentView(R.layout.activity_main);

        videoView = findViewById(R.id.videoView);
        videoTitle = findViewById(R.id.videoTitle);
        playPauseToggle = findViewById(R.id.playPauseToggle);
        Button selectBtn = findViewById(R.id.selectVideoBtn);
        Button stopBtn = findViewById(R.id.stopBtn);

        playPauseToggle.setEnabled(false);

        // Setup media controls inside video view
        MediaController controller = new MediaController(this);
        controller.setAnchorView(videoView);
        videoView.setMediaController(controller);

        ActivityResultLauncher<Intent> videoPicker = registerForActivityResult(
                new ActivityResultContracts.StartActivityForResult(),
                result -> {
                    if (result.getResultCode() == RESULT_OK && result.getData() != null) {
                        selectedVideo = result.getData().getData();
                        if (selectedVideo != null) {
                            videoName = getFileName(selectedVideo);
                            videoTitle.setText("Selected: " + videoName);
                            videoView.setVideoURI(selectedVideo);
                            playPauseToggle.setEnabled(true);
                        }
                    }
                }
        );

        selectBtn.setOnClickListener(v -> {
            Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
            intent.setType("video/*");
            videoPicker.launch(Intent.createChooser(intent, "Pick a video file"));
        });

        playPauseToggle.setOnCheckedChangeListener((btn, isChecked) -> {
            if (selectedVideo == null) {
                Toast.makeText(this, "Please select a video first!", Toast.LENGTH_SHORT).show();
                playPauseToggle.setChecked(false);
                return;
            }

            if (isChecked) {
                videoView.start();
                videoTitle.setText("Playing: " + videoName);
            } else {
                videoView.pause();
                videoTitle.setText("Paused: " + videoName);
            }
        });

        stopBtn.setOnClickListener(v -> {
            if (videoView.isPlaying()) {
                videoView.stopPlayback();
                videoView.setVideoURI(selectedVideo); // reset
                videoTitle.setText("Stopped: " + videoName);
                playPauseToggle.setChecked(false);
            }
        });

        videoView.setOnCompletionListener(mp -> {
            videoTitle.setText("Finished: " + videoName);
            playPauseToggle.setChecked(false);
        });
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
}
