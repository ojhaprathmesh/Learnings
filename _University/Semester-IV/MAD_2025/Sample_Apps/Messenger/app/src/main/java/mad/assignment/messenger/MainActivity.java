package mad.assignment.messenger;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.telephony.SmsManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class MainActivity extends AppCompatActivity {
    private EditText phoneInput, messageInput;
    private TextView receivedSmsText;
    private static final int PERMISSION_CODE = 123;

    @SuppressLint("StaticFieldLeak")
    public static MainActivity instance;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        phoneInput = findViewById(R.id.phoneInput);
        messageInput = findViewById(R.id.messageInput);
        receivedSmsText = findViewById(R.id.receivedSmsText);
        Button sendBtn = findViewById(R.id.sendBtn);

        if (!hasPermissions()) {
            ActivityCompat.requestPermissions(this,
                    new String[]{
                            Manifest.permission.SEND_SMS,
                            Manifest.permission.RECEIVE_SMS,
                            Manifest.permission.READ_SMS
                    }, PERMISSION_CODE);
        }

        sendBtn.setOnClickListener(v -> sendSMS());
    }

    private void sendSMS() {
        String phone = phoneInput.getText().toString().trim();
        String message = messageInput.getText().toString().trim();

        if (phone.isEmpty() || message.isEmpty()) {
            Toast.makeText(this, "Phone or message can't be empty", Toast.LENGTH_SHORT).show();
            return;
        }

        try {
            SmsManager.getDefault().sendTextMessage(phone, null, message, null, null);
            Toast.makeText(this, "SMS Sent!", Toast.LENGTH_SHORT).show();
        } catch (Exception e) {
            Toast.makeText(this, "Failed to send SMS", Toast.LENGTH_SHORT).show();
        }
    }

    private boolean hasPermissions() {
        return ContextCompat.checkSelfPermission(this, Manifest.permission.SEND_SMS) == PackageManager.PERMISSION_GRANTED
                && ContextCompat.checkSelfPermission(this, Manifest.permission.RECEIVE_SMS) == PackageManager.PERMISSION_GRANTED
                && ContextCompat.checkSelfPermission(this, Manifest.permission.READ_SMS) == PackageManager.PERMISSION_GRANTED;
    }

    public void updateReceivedText(String msg) {
        receivedSmsText.setText("Received:\n" + msg);
    }

    @Override
    protected void onResume() {
        super.onResume();
        instance = this;
    }

    @Override
    protected void onPause() {
        super.onPause();
        instance = null;
    }
}
