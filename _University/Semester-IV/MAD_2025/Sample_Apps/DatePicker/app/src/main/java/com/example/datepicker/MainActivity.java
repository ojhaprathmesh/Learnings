package com.example.datepicker;

import android.os.Bundle;
import android.widget.DatePicker;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    DatePicker datePicker;
    TextView tvSelectedDate;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        datePicker = findViewById(R.id.datePicker);
        tvSelectedDate = findViewById(R.id.tvSelectedDate);

        updateDateText(datePicker.getYear(), datePicker.getMonth(), datePicker.getDayOfMonth());

        datePicker.setOnDateChangedListener((view, year, monthOfYear, dayOfMonth) ->
                updateDateText(year, monthOfYear, dayOfMonth)
        );
    }

    private void updateDateText(int year, int month, int day) {
        String date = day + "/" + (month + 1) + "/" + year;
        tvSelectedDate.setText("Selected Date: " + date);
    }
}
