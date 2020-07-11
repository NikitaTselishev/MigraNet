package com.example.migranet;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
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

public class LoginActivity extends AppCompatActivity {
    EditText email_view;
    EditText password_view;


    TextView status_view;
    public static String session="";
    public static String error="";
    public static String user_id="";

    public void goto_register(View view){
        Intent intent = new Intent(LoginActivity.this, RegisterActivity.class);
        startActivity(intent);
    }
    public void login(View view) throws JSONException {

        String login = email_view.getText().toString();
        String password = password_view.getText().toString();




        JSONObject user = new JSONObject();
        try {
            user.put("email", login);
            user.put("password", password);
        } catch (JSONException e){
            e.printStackTrace();
        }

        final JSONObject login_request = new JSONObject();
        try{
            login_request.put("jsonrpc", "2.0");
            login_request.put("id", 777);
            login_request.put("method", "user.login_by_email");
            login_request.put("params",user);
        } catch (JSONException e){
            e.printStackTrace();
        }


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
                    output_stream.write(login_request.toString().getBytes());
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
                                if (answer.has("result")){
                                    Log.v(null,answer.toString());
                                    //status_view.setText("Your user session is "+answer.getJSONObject("result").getString("user_session"));
                                    session=answer.getJSONObject("result").getString("user_session");
                                    user_id=answer.getJSONObject("result").getString("user_id");

                                } else{
                                    if (answer.has("error")) {
                                        error=answer.getJSONObject("error").getString("message");
                                    }
                                }
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


        if(session!=""){
            ((MigraNet)this.getApplication()).setSession(session);
            ((MigraNet)this.getApplication()).setUserId(user_id);
            Intent intent = new Intent(LoginActivity.this, MainActivity.class);
            startActivity(intent);
        }
        if (error!=""){
            status_view.setText(error);
        }
    }
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        email_view = (EditText)findViewById(R.id.email);
        password_view = (EditText)findViewById(R.id.password);

        status_view = (TextView)findViewById(R.id.status_view);



    }
}