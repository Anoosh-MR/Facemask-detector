package com.example.facemaskdetection;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class IPSET extends AppCompatActivity {
    EditText e1;
    Button b1;
    SharedPreferences sh;
    String ip;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ipset);

        sh = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());

        e1=findViewById(R.id.editTextTextPersonName6);
        b1=findViewById(R.id.button9);
        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                ip = e1.getText().toString();
                if (ip.equalsIgnoreCase("")) {
                    e1.setError("Enter Your ip");
                }
                else {


                    SharedPreferences.Editor edp = sh.edit();
                    edp.putString("ip", ip);
                    edp.commit();
                    Intent i = new Intent(getApplicationContext(), LOGIN.class);
                    startActivity(i);

                }
                }


        });



    }
}