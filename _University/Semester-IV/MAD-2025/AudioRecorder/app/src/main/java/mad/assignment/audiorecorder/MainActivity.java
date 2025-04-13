package mad.assignment.audiorecorder;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.MediaRecorder;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.provider.Settings;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {
    private static final int PERMISSION_CODE = 101;

    private MediaRecorder recorder;
    private boolean isRecording = false;
    private String filePath;

    private Button recordBtn;
    private TextView statusText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        recordBtn = findViewById(R.id.recordBtn);
        statusText = findViewById(R.id.statusText);

        recordBtn.setOnClickListener(v -> {
            if (!hasPermissions()) {
                requestPermissions();
                return;
            }

            if (isRecording) stopRecording();
            else startRecording();
        });
    }

    private boolean hasPermissions() {
        boolean micPermission = ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) == PackageManager.PERMISSION_GRANTED;
        boolean storagePermission = Build.VERSION.SDK_INT >= Build.VERSION_CODES.R
                ? Environment.isExternalStorageManager()
                : ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) == PackageManager.PERMISSION_GRANTED;

        return micPermission && storagePermission;
    }

    private void requestPermissions() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            Intent intent = new Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION);
            intent.setData(Uri.parse("package:" + getPackageName()));
            startActivity(intent);
        } else {
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.RECORD_AUDIO, Manifest.permission.WRITE_EXTERNAL_STORAGE},
                    PERMISSION_CODE);
        }
    }

    @SuppressLint("SetTextI18n")
    private void startRecording() {
        File dir = new File(Environment.getExternalStorageDirectory(), "Recordings/MAD_Audio_Recorder");
        if (!dir.exists() && !dir.mkdirs()) {
            Toast.makeText(this, "Failed to create directory", Toast.LENGTH_SHORT).show();
            return;
        }

        String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.getDefault()).format(new Date());
        filePath = new File(dir, "recording_" + timestamp + ".3gp").getAbsolutePath();

        recorder = new MediaRecorder();
        recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        recorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);
        recorder.setOutputFile(filePath);

        try {
            recorder.prepare();
            recorder.start();
            isRecording = true;
            recordBtn.setText("Stop Recording");
            statusText.setText("Recording...");
        } catch (Exception e) {
            Toast.makeText(this, "Recording failed to start", Toast.LENGTH_SHORT).show();
        }
    }

    @SuppressLint("SetTextI18n")
    private void stopRecording() {
        try {
            recorder.stop();
        } catch (Exception ignored) {}

        recorder.release();
        recorder = null;
        isRecording = false;

        recordBtn.setText("Start Recording");
        statusText.setText("Saved to:\n" + filePath);
    }

    @Override
    protected void onDestroy() {
        if (recorder != null) recorder.release();
        super.onDestroy();
    }
}
