package com.example.facemaskdetection;

import androidx.appcompat.app.AppCompatActivity;

import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.TextView;

import java.util.ArrayList;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.drawable.Drawable;
import android.os.StrictMode;
import android.preference.PreferenceManager;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.Spinner;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

public class VIEWCOURSE extends AppCompatActivity  implements AdapterView.OnItemSelectedListener {

    Spinner s1;
    Button b3;
    SharedPreferences sh;
    ListView l1;
    String url,depid,url2;
    ArrayList<String> depname,did,course;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_viewcourse);
        sh = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        s1=findViewById(R.id.spinner);
        b3=findViewById(R.id.button6);
        l1=findViewById(R.id.a);


        url ="http://"+sh.getString("ip","")+":5000/viewdep";
        s1.setOnItemSelectedListener(VIEWCOURSE.this);
        RequestQueue queue = Volley.newRequestQueue(VIEWCOURSE.this);

        StringRequest stringRequest = new StringRequest(Request.Method.POST, url,new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                // Display the response string.
                Log.d("+++++++++++++++++",response);
                try {

                    JSONArray ar=new JSONArray(response);

                    depname= new ArrayList<>(ar.length());
                    did= new ArrayList<>(ar.length());
                    for(int i=0;i<ar.length();i++)
                    {
                        JSONObject jo=ar.getJSONObject(i);
                        depname.add(jo.getString("department"));
                        did.add(jo.getString("did"));


                    }

                    ArrayAdapter<String> ad=new ArrayAdapter<>(VIEWCOURSE.this,android.R.layout.simple_spinner_item,depname);
                    s1.setAdapter(ad);

                    // l1.setAdapter(new custom2(Monitoring_signal.this,notification,date));

                } catch (JSONException e) {
                    e.printStackTrace();
                }


            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

                Toast.makeText(getApplicationContext(),"Error",Toast.LENGTH_LONG).show();
            }
        });
        // Add the request to the RequestQueue.
        queue.add(stringRequest);


        b3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {


                url2 ="http://"+sh.getString("ip", "") + ":5000/viewcourse";
                RequestQueue queue1 = Volley.newRequestQueue(VIEWCOURSE.this);

                StringRequest stringRequest1 = new StringRequest(Request.Method.POST, url2,new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the response string.
                        Log.d("+++++++++++++++++",response);
                        try {

                            JSONArray ar=new JSONArray(response);
                            course= new ArrayList<>();


                            for(int i=0;i<ar.length();i++)
                            {
                                JSONObject jo=ar.getJSONObject(i);
                                course.add(jo.getString("coursename"));


                            }

                            ArrayAdapter<String> ad=new ArrayAdapter<String>(VIEWCOURSE.this,android.R.layout.simple_list_item_1,course);
                            l1.setAdapter(ad);

                        } catch (Exception e) {
                            Log.d("=========", e.toString());
                        }


                    }

                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {

                        Toast.makeText(VIEWCOURSE.this, "err"+error, Toast.LENGTH_SHORT).show();
                    }
                }) {
                    @Override
                    protected Map<String, String> getParams() {
                        Map<String, String> params = new HashMap<>();
                        params.put("did", depid);

                        return params;
                    }
                };
                queue1.add(stringRequest1);







            }
        });
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
        depid=did.get(position);





    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }
    @Override
    public void onBackPressed() {
        super.onBackPressed();
        Intent ik = new Intent(getApplicationContext(), HOME.class);
        startActivity(ik);
    }
}