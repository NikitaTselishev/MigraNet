package com.example.migranet;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;

public class AddEventActivity extends AppCompatActivity {
    EditText name_view;
    EditText description_view;
    EditText time_view;

    TextView status_view;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_event);

        name_view = (EditText)findViewById(R.id.name_view);
        description_view = (EditText)findViewById(R.id.description_view);
        time_view = (EditText)findViewById(R.id.time_view);

        status_view = (TextView)findViewById(R.id.status_view);
    }

    public void create_event(View view){
        String name = name_view.getText().toString();
        String description = description_view.getText().toString();
        String time = time_view.getText().toString();

        LocationManager lm = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        @SuppressLint("MissingPermission") Location location = lm.getLastKnownLocation(LocationManager.GPS_PROVIDER);
        final double longitude = location.getLongitude();
        final double latitude = location.getLatitude();



        String session=((MigraNet)this.getApplication()).getSession();


        //forming user json
        JSONObject event = new JSONObject();
        try {
            event.put("user_session", Integer.parseInt(session));
            event.put("name", name);
            event.put("description", description);
            event.put("latitude", latitude);
            event.put("longitude", longitude);
            event.put("action_time", Integer.parseInt(time));
        } catch (JSONException e){
            e.printStackTrace();
        }

        //forming register_request json
        final JSONObject request = new JSONObject();
        try{
            request.put("jsonrpc", "2.0");
            request.put("id", 777);
            request.put("method", "action.create");
            request.put("params",event);
        } catch (JSONException e){
            e.printStackTrace();
        }

        status_view.setText(request.toString());

        //starting new request
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

    public void goto_events(View view){
        Intent intent = new Intent(AddEventActivity.this, EventsActivity.class);
        startActivity(intent);

    }
}