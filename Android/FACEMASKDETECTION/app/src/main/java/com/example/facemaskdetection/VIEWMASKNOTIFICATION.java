package com.example.facemaskdetection;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class VIEWMASKNOTIFICATION extends AppCompatActivity {
    ListView lv2;
    SharedPreferences sh;
    ArrayList<String> date,notification;
    String url2;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_viewmasknotification);
        sh = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        lv2=findViewById(R.id.listv);
        url2 ="http://"+sh.getString("ip", "") + ":5000/viewcamnotification";
        RequestQueue queue1 = Volley.newRequestQueue(VIEWMASKNOTIFICATION.this);

        StringRequest stringRequest1 = new StringRequest(Request.Method.POST, url2,new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                // Display the response string.
                Log.d("+++++++++++++++++",response);
                try {

                    JSONArray ar=new JSONArray(response);
                    date= new ArrayList<>();
                    notification=new ArrayList<>();


                    for(int i=0;i<ar.length();i++)
                    {
                        JSONObject jo=ar.getJSONObject(i);
                       notification.add(jo.getString("image"));
                        date.add(jo.getString("datetime"));


                    }
/*
                    ArrayAdapter<String> ad=new ArrayAdapter<String>(VIEWMASKNOTIFICATION.this,android.R.layout.simple_list_item_1,course);
                    lv2.setAdapter(ad);*/

                    lv2.setAdapter(new custom_image(VIEWMASKNOTIFICATION.this,notification,date));



                } catch (Exception e) {
                    Log.d("=========", e.toString());
                }


            }

        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

                Toast.makeText(VIEWMASKNOTIFICATION.this, "err"+error, Toast.LENGTH_SHORT).show();
            }
        }) {
            @Override
            protected Map<String, String> getParams() {
                Map<String, String> params = new HashMap<>();
                params.put("lid", sh.getString("lid",""));

                return params;
            }
        };
        queue1.add(stringRequest1);






    }
    @Override
    public void onBackPressed() {
        super.onBackPressed();
        Intent ik = new Intent(getApplicationContext(), HOME.class);
        startActivity(ik);
    }
}