package mad.assignment.notifier;

import android.Manifest;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.RequiresPermission;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

public class MainActivity extends AppCompatActivity {
    private static final String CHANNEL_ID = "demo_channel_id";
    private static final int NOTIFICATION_ID = 101;
    private static final int PERMISSION_REQUEST_CODE = 100;

    private EditText messageInput;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        messageInput = findViewById(R.id.messageInput);
        Button sendButton = findViewById(R.id.sendNotificationBtn);

        createNotificationChannel();

        sendButton.setOnClickListener(v -> {
            String message = messageInput.getText().toString().trim();

            if (message.isEmpty()) {
                Toast.makeText(this, "Enter a message", Toast.LENGTH_SHORT).show();
                return;
            }

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
                    ActivityCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.POST_NOTIFICATIONS}, PERMISSION_REQUEST_CODE);
                return;
            }

            showNotification(message);
        });
    }

    @RequiresPermission(Manifest.permission.POST_NOTIFICATIONS)
    private void showNotification(String message) {
        Intent intent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(this, 0, intent,
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);

        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(android.R.drawable.ic_dialog_info)
                .setContentTitle("MAD Notification")
                .setContentText(message)
                .setContentIntent(pendingIntent)
                .setAutoCancel(true)
                .setPriority(NotificationCompat.PRIORITY_DEFAULT);

        NotificationManagerCompat.from(this).notify(NOTIFICATION_ID, builder.build());
        Toast.makeText(this, "Notification sent!", Toast.LENGTH_SHORT).show();
    }

    private void createNotificationChannel() {
        NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID, "MAD Notifications", NotificationManager.IMPORTANCE_DEFAULT);
        channel.setDescription("Notification Channel for MAD");

        NotificationManager manager = getSystemService(NotificationManager.class);
        manager.createNotificationChannel(channel);
    }
}
