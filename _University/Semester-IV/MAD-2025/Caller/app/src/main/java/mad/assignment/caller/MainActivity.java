package mad.assignment.caller;

import android.Manifest;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

public class MainActivity extends AppCompatActivity {

    EditText phoneNumber;
    Button callButton;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        phoneNumber = findViewById(R.id.phoneNumber);
        callButton = findViewById(R.id.callButton);

        ActivityCompat.requestPermissions(this,
                new String[]{Manifest.permission.CALL_PHONE, Manifest.permission.READ_PHONE_STATE},
                1);

        callButton.setOnClickListener(v -> {
            String number = phoneNumber.getText().toString().trim();
            if (!number.isEmpty()) {
                Intent callIntent = new Intent(Intent.ACTION_CALL);
                callIntent.setData(Uri.parse("tel:" + number));
                startActivity(callIntent);
            } else {
                Toast.makeText(this, "Enter a phone number", Toast.LENGTH_SHORT).show();
            }
        });
    }
}
