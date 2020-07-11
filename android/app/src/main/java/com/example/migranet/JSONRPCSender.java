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
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;


public class JSONRPCSender {

    URL address;
    ExecutorService executor;

    public JSONRPCSender(String address){
        URL url = null;
        this.executor = Executors.newSingleThreadExecutor();
        try {
            this.address = new URL("http://81.91.176.31:9989/");
        } catch (MalformedURLException e) {
            e.printStackTrace();
            this.address = url;
        }
    }

    public JSONObject get_json_rpc_template(){
        JSONObject register_request = new JSONObject();
        try{
            register_request.put("jsonrpc", "2.0");
            register_request.put("id", 0);
        } catch (JSONException e){
            e.printStackTrace();
        }
        return register_request;
    }

    public Future<JSONObject> send_json(String method, JSONObject params){
        JSONObject request = this.get_json_rpc_template();
        try {
            request.put("method", method);
            request.put("params", params);
        } catch (JSONException e){
            e.printStackTrace();
        }
        Callable<JSONObject> task = () -> {
            HttpURLConnection urlConnection = null;
            try {
                urlConnection = (HttpURLConnection) this.address.openConnection();
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
                try {
                    return new JSONObject(decodedString);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                urlConnection.disconnect();
            }
            return new JSONObject();
        };
        return this.executor.submit(task);
    }
}
