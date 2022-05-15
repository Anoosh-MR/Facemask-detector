package com.example.facemaskdetection;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.ListView;
import android.widget.TextView;

public class VIEWDEPARTMENT extends AppCompatActivity {
    TextView tv1;
    ListView l1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_viewdepartment);
        tv1=findViewById(R.id.textView);
        l1=findViewById(R.id.list);

    }
    @Override
    public void onBackPressed() {
        super.onBackPressed();
        Intent ik = new Intent(getApplicationContext(), HOME.class);
        startActivity(ik);
    }
}