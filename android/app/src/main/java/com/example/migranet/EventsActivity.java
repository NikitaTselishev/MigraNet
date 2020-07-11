package com.example.migranet;

import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.w3c.dom.Text;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;

public class EventsActivity extends AppCompatActivity {
    //TextView status_view;
    LinearLayout layout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_events);

        //status_view = (TextView) findViewById(R.id.status_view);
        layout = (LinearLayout) findViewById(R.id.events);


        try {
            find_events(null);
        } catch (JSONException e) {
            e.printStackTrace();
        }

    }


    public void find_events(View view) throws JSONException {

        layout.removeAllViews();

        LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        @SuppressLint("MissingPermission") Location location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
        final double longitude = location.getLongitude();
        final double latitude = location.getLatitude();



        String session=((MigraNet)this.getApplication()).getSession();




        JSONObject filter = new JSONObject();
        try {
            filter.put("user_session", Long.parseLong(session));
            filter.put("latitude", latitude);
            filter.put("longitude", longitude);
            filter.put("r", 100);
        } catch (JSONException e){
            e.printStackTrace();
        }

        final JSONObject request = new JSONObject();
        try{
            request.put("jsonrpc", "2.0");
            request.put("id", 777);
            request.put("method", "action.find");
            request.put("params",filter);
        } catch (JSONException e){
            e.printStackTrace();
        }

        Log.v(null,"Requested "+request.toString());

        new Thread(new Runnable() {
            public void run() {
                URL url = null;
                try {
                    url = new URL("http://81.91.176.31:9989/");
                } catch (MalformedURLException e) {
                    e.printStackTrace();
                }
                HttpURLConnection urlConnection = null;
                try {
                    urlConnection = (HttpURLConnection) url.openConnection();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                urlConnection.setDoOutput(true);
                try {
                    urlConnection.setRequestMethod("POST");
                } catch (ProtocolException e) {
                    e.printStackTrace();
                }
                try {
                    urlConnection.connect();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                try{
                    OutputStream output_stream = urlConnection.getOutputStream();
                    output_stream.write(request.toString().getBytes());
                    output_stream.flush();
                    output_stream.close();


                    BufferedReader in = new BufferedReader(
                            new InputStreamReader(
                                    urlConnection.getInputStream()));
                    final String decodedString=in.readLine();

                    final String response = urlConnection.getResponseMessage();
                    runOnUiThread(new Runnable(){
                        @Override
                        public void run(){
                            //status_view.setText(decodedString);
                            try {
                                JSONObject answer = new JSONObject(decodedString);
                                Log.v(null,decodedString);
                                String test_text=answer.getString("result");
                                JSONArray items = new JSONArray(test_text);

                                LayoutInflater inflater = getLayoutInflater();

                                for (int i=0;i<items.length();i++){
                                    JSONObject item = items.getJSONObject(i);

                                    View new_view = inflater.inflate(R.layout.event,layout);

                                    CardView card_view =(CardView) layout.getChildAt(i);
                                    card_view.setTag(item.getString("action_id"));
                                    TextView name_view = (TextView)   ((CardView)card_view).getChildAt(0);
                                    name_view.setText(item.getString("name"));
                                    TextView description_view = (TextView)   ((CardView)card_view).getChildAt(1);
                                    description_view.setText(item.getString("description"));
                                }
                                //status_view.setText(answer.toString());
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }

                        }

                    });


                } catch (UnsupportedEncodingException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                } finally {
                    urlConnection.disconnect();
                }

            }
        }).start();




    }


    public void chose_event(View view){
        ((MigraNet)this.getApplication()).setEvent(view.getTag().toString());
        Intent intent = new Intent(EventsActivity.this, EventInfoActivity.class);
        startActivity(intent);
    }

    public void goto_home(View view){
        Intent intent = new Intent(EventsActivity.this, MainActivity.class);
        startActivity(intent);

    }
    public void goto_add_event(View view){
        Intent intent = new Intent(EventsActivity.this, AddEventActivity.class);
        startActivity(intent);

    }
}