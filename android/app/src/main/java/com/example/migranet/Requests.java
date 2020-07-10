package com.example.migranet;

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

public class Requests {
    public static String response;

    public String getResponse(final String request,final String url_string){

        response="";
        new Thread(new Runnable() {
            public void run() {
                URL url = null;
                try {
                    url = new URL(url_string);//"http://81.91.176.31:9989/");
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
                    final String response=in.readLine();

//                    runOnUiThread(new Runnable(){
//                        @Override
//                        public void run(){
//                            //status_view.setText(decodedString);
//                            try {
//                                JSONObject answer = new JSONObject(decodedString);
//                                if (answer.has("result")){
//                                    //status_view.setText("Your user session is "+answer.getJSONObject("result").getString("user_session"));
//                                    session=answer.getJSONObject("result").getString("user_session");
//                                } else{
//                                    if (answer.has("error")) {
//                                        error=answer.getJSONObject("error").getString("message");
//                                    }
//                                }
//                            } catch (JSONException e) {
//                                e.printStackTrace();
//                            }
//
//                        }
//
//                    });


                } catch (UnsupportedEncodingException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                } finally {
                    urlConnection.disconnect();
                }

            }
        }).start();
        return response;
    }
}
