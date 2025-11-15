package mad.assignment.emailapp;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {

    private EditText emailEditText, subjectEditText, messageEditText;
    private Button sendButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_main);
        
        // Initialize views
        emailEditText = findViewById(R.id.emailEditText);
        subjectEditText = findViewById(R.id.subjectEditText);
        messageEditText = findViewById(R.id.messageEditText);
        sendButton = findViewById(R.id.sendButton);
        
        // Set window insets listener
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });
        
        // Set click listener for send button
        sendButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendEmail();
            }
        });
    }
    
    private void sendEmail() {
        String email = emailEditText.getText().toString().trim();
        String subject = subjectEditText.getText().toString().trim();
        String message = messageEditText.getText().toString().trim();
        
        // Validate input fields
        if (email.isEmpty()) {
            emailEditText.setError("Email address is required");
            return;
        }
        
        // Create intent to send email
        Intent intent = new Intent(Intent.ACTION_SEND);
        intent.putExtra(Intent.EXTRA_EMAIL, new String[]{email});
        intent.putExtra(Intent.EXTRA_SUBJECT, subject);
        intent.putExtra(Intent.EXTRA_TEXT, message);
        
        // Set type to email
        intent.setType("message/rfc822");
        
        try {
            // Start email client
            startActivity(Intent.createChooser(intent, "Choose an Email client"));
        } catch (android.content.ActivityNotFoundException ex) {
            Toast.makeText(MainActivity.this, 
                    "There are no email clients installed.", Toast.LENGTH_SHORT).show();
        }
    }
}