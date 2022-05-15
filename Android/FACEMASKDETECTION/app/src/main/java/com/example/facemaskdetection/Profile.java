package com.example.facemaskdetection;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.widget.ImageView;
import android.widget.TextView;

import com.android.volley.toolbox.StringRequest;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.drawable.Drawable;
import android.os.StrictMode;
import android.util.Log;
import android.util.Patterns;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
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

import java.util.HashMap;
import java.util.Map;
public class Profile extends AppCompatActivity {
    TextView TV1,TV2,TV3,TV4,TV5,TV6;
    ImageView I1;
    SharedPreferences sh;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);
        sh = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
        TV1=findViewById(R.id.textView7);
        TV2=findViewById(R.id.textView10);
        TV3=findViewById(R.id.textView12);
        TV4=findViewById(R.id.textView15);
        TV5=findViewById(R.id.textView17);
        TV6=findViewById(R.id.textView19);
        I1=findViewById(R.id.imageView);
        RequestQueue queue = Volley.newRequestQueue(Profile.this);
      String  url1 = "http://" + sh.getString("ip", "") + ":5000/viewprofile";
        StringRequest stringRequest = new StringRequest(Request.Method.POST, url1,new Response.Listener<String>() {
            @SuppressLint("SetTextI18n")
            @Override
            public void onResponse(String response) {
                // Display the response string.
                Log.d("+++++++++++++++++",response);
                try {

                    JSONArray ar=new JSONArray(response);

                    {
                        JSONObject jo=ar.getJSONObject(0);
                        TV1.setText(jo.getString("fname")+" "+jo.getString("lname"));
                        TV2.setText(jo.getString("age"));
                        TV3.setText(jo.getString("gender"));
                        TV4.setText(jo.getString("phone"));
                        TV5.setText(jo.getString("email"));
                        TV6.setText(jo.getString("place")+" "+jo.getString("post")+" "+jo.getString("pin"));


                        if (android.os.Build.VERSION.SDK_INT > 9) {
                            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
                            StrictMode.setThreadPolicy(policy);
                        }


//        i2.setImageDrawable(Drawable.createFromPath(getIntent().getStringExtra("photo"))));
                        java.net.URL thumb_u;
                        try {

                            //thumb_u = new java.net.URL("http://192.168.43.57:5000/static/photo/flyer.jpg");

                            thumb_u = new java.net.URL("http://"+sh.getString("ip","")+":5000/static/student pic/"+jo.getString("photo"));
                            Drawable thumb_d = Drawable.createFromStream(thumb_u.openStream(), "src");
                            I1.setImageDrawable(thumb_d);

                        }
                        catch (Exception e)
                        {
                            Log.d("errsssssssssssss",""+e);
                        }
                    }


                } catch (JSONException e) {
                    e.printStackTrace();
                }

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {

                Toast.makeText(getApplicationContext(),"Error",Toast.LENGTH_LONG).show();
            }
        }){
            @Override
            protected Map<String, String> getParams()
            {
                Map<String, String>  params = new HashMap<String, String>();

                params.put("uid", sh.getString("lid", ""));


                return params;
            }
        };
        // Add the request to the RequestQueue.
        queue.add(stringRequest);


    }
    @Override
    public void onBackPressed() {
        super.onBackPressed();
        Intent ik = new Intent(getApplicationContext(), HOME.class);
        startActivity(ik);
    }
}