package mad.assignment.camera;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.FileProvider;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class MainActivity extends AppCompatActivity {

    static final int REQUEST_IMAGE_CAPTURE = 1;
    String currentPhotoPath;
    ImageView imageView;
    Button captureButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        imageView = findViewById(R.id.capturedImage);
        captureButton = findViewById(R.id.captureBtn);

        captureButton.setOnClickListener(v -> dispatchTakePictureIntent());
    }

    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        // Ensure the Intent can be resolved
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            File photoFile = null;

            try {
                photoFile = createImageFile();
            } catch (IOException ex) {
                ex.printStackTrace();
                Toast.makeText(this, "Error creating image file", Toast.LENGTH_SHORT).show();
                return;
            }

            if (photoFile != null) {
                try {
                    Uri photoURI = FileProvider.getUriForFile(this,
                            getPackageName() + ".fileprovider", photoFile);
                    takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoURI);
                    startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
                } catch (Exception e) {
                    e.printStackTrace();
                    Toast.makeText(this, "Error starting camera: " + e.getMessage(), 
                            Toast.LENGTH_SHORT).show();
                }
            }
        } else {
            Toast.makeText(this, "No camera app available on this device", 
                    Toast.LENGTH_SHORT).show();
        }
    }

    private File createImageFile() throws IOException {
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());
        String imageFileName = "JPEG_" + timeStamp + "_";
        File storageDir = getExternalFilesDir("Pictures");
        File image = File.createTempFile(
                imageFileName,  /* prefix */
                ".jpg",    /* suffix */
                storageDir     /* directory */
        );
        currentPhotoPath = image.getAbsolutePath();
        return image;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            imageView.setImageURI(Uri.fromFile(new File(currentPhotoPath)));
            
            galleryAddPic();
        }
    }
    
    private void galleryAddPic() {
        try {
            File f = new File(currentPhotoPath);
            if (!f.exists()) {
                Toast.makeText(this, "Image file not found", Toast.LENGTH_SHORT).show();
                return;
            }
            
            // Method 1: Use ACTION_MEDIA_SCANNER_SCAN_FILE intent
            Intent mediaScanIntent = new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE);
            Uri contentUri = Uri.fromFile(f);
            mediaScanIntent.setData(contentUri);
            sendBroadcast(mediaScanIntent);
            
            // Method 2: Use MediaStore to insert the image
            try {
                MediaStore.Images.Media.insertImage(
                        getContentResolver(),
                        currentPhotoPath,
                        f.getName(),
                        "Image captured by Camera App"
                );
            } catch (Exception insertError) {
                // If insertion fails, log but continue - the first method might still work
                insertError.printStackTrace();
            }
            
            Toast.makeText(this, "Image saved to gallery", Toast.LENGTH_SHORT).show();
        } catch (Exception e) {
            e.printStackTrace();
            Toast.makeText(this, "Failed to save image to gallery: " + e.getMessage(), 
                    Toast.LENGTH_SHORT).show();
        }
    }
}
