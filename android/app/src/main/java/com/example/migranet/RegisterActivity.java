package com.example.migranet;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
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

public class RegisterActivity extends AppCompatActivity {
    EditText first_name_view;
    EditText second_name_view;
    EditText birth_date_view;
    EditText email_view;
    EditText phone_view;
    EditText password_view;

    TextView status_view;
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        first_name_view = (EditText)findViewById(R.id.first_name);
        second_name_view = (EditText)findViewById(R.id.second_name);
        birth_date_view = (EditText)findViewById(R.id.birth_date);
        email_view = (EditText)findViewById(R.id.email);
        phone_view = (EditText)findViewById(R.id.phone);
        password_view = (EditText)findViewById(R.id.password);

        status_view = (TextView)findViewById(R.id.status);
    }

    public void register(View view){
        String first_name = first_name_view.getText().toString();
        String second_name = second_name_view.getText().toString();
        String birth_date = birth_date_view.getText().toString();
        String email = email_view.getText().toString();
        String phone = phone_view.getText().toString();
        String password = password_view.getText().toString();


        //forming user json
        JSONObject user = new JSONObject();
        try {
            user.put("first_name", first_name);
            user.put("second_name", second_name);
            user.put("birthday", birth_date);
            user.put("email", email);
            user.put("phone", phone);
            user.put("password", password);
        } catch (JSONException e){
            e.printStackTrace();
        }

        //forming register_request json
        final JSONObject register_request = new JSONObject();
        try{
            register_request.put("jsonrpc", "2.0");
            register_request.put("id", 777);
            register_request.put("method", "user.create");
            register_request.put("params",user);
        } catch (JSONException e){
            e.printStackTrace();
        }

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
                    output_stream.write(register_request.toString().getBytes());
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
                            status_view.setText(decodedString);
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

        //Intent intent = new Intent(RegisterActivity.this, LoginActivity.class);
        //startActivity(intent);
    }
}