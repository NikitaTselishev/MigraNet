package com.example.migranet;

import com.example.migranet.JSONRPCSender;
import androidx.appcompat.app.AppCompatActivity;
import androidx.cardview.widget.CardView;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.Arrays;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;


public class EventInfoActivity extends AppCompatActivity {

    //ScheduledExecutorService ses;

    TextView name_view;
    TextView description_view;
    TextView time_view;
    TextView place_view;
    Button send_button;

    ScrollView scroll_view;

    EditText message_view;

    LinearLayout layout;

    String event_id;
    String session;
    static String user_id;
    public static Boolean is_member;
    public static String action_id;

    static String chat;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_event_info);

        event_id = ((MigraNet)this.getApplication()).getEvent();
        session = ((MigraNet)this.getApplication()).getSession();
        user_id = ((MigraNet)this.getApplication()).getUserId();


        name_view = (TextView)findViewById(R.id.name_view);
        description_view = (TextView)findViewById(R.id.description_view);
        time_view = (TextView)findViewById(R.id.time_view);
        place_view =(TextView)findViewById(R.id.place_view);
        layout = (LinearLayout)findViewById(R.id.layout);
        message_view = (EditText) findViewById(R.id.message_view);
        send_button = (Button)findViewById(R.id.send);
        scroll_view = (ScrollView)findViewById(R.id.scroll_view);
        name_view.setText(event_id);
        refresh(null);

        //ses = Executors.newSingleThreadScheduledExecutor();

//        ses.scheduleAtFixedRate(new Runnable() {
//            @Override
//            public void run() {
//                refresh(null);
//            }
//        }, 0, 10, TimeUnit.SECONDS);


    }

//    protected void onDestroy() {
//        super.onDestroy();
//        ses.shutdown();
//    }

    public void click_send(View view){
        if (is_member){
            send_message(null);
        } else{
            join_event(null);
        }
    }

    public void join_event(View view){
        JSONObject params = new JSONObject();
        try {
            params.put("user_session", Long.parseLong(session));
            params.put("action_id", Long.parseLong(action_id));
        } catch (JSONException e){
            e.printStackTrace();
        }
        JSONRPCSender sender = new JSONRPCSender("http://81.91.176.31:9989/");
        Future<JSONObject> result = sender.send_json("user.add_to_action", params);
        try {
            JSONObject answer = result.get();
            //time_view.setText(params.toString()+"\n"+answer.toString());

            Log.v(null,params.toString());
            Log.v(null,answer.toString());
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        refresh(null);
    }
    public void send_message(View view){

        String message = message_view.getText().toString();
        JSONObject params = new JSONObject();
        try {
            params.put("user_session", Long.parseLong(session));
            params.put("chat_id", Long.parseLong(chat));
            params.put("message", message);
        } catch (JSONException e){
            e.printStackTrace();
        }
        JSONRPCSender sender = new JSONRPCSender("http://81.91.176.31:9989/");
        Future<JSONObject> result = sender.send_json("chat.send_message", params);
        try {
            JSONObject answer = result.get();
            //time_view.setText(params.toString()+"\n"+answer.toString());

            Log.v(null,params.toString());
            Log.v(null,answer.toString());
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        refresh(null);

    }

    public void refresh(View view){
        layout.removeAllViews();


        JSONObject params = new JSONObject();
        try {
            params.put("user_session", Long.parseLong(session));
            params.put("action_id", Long.parseLong(event_id));
        } catch (JSONException e){
            e.printStackTrace();
        }

        JSONRPCSender sender = new JSONRPCSender("http://81.91.176.31:9989/");
        Future<JSONObject> result = sender.send_json("action.get", params);
        runOnUiThread(new Runnable(){
            @Override
            public void run(){
                try {
                    JSONObject answer = result.get();
                    if (answer.has("result")){
                        answer = new JSONObject(answer.getString("result"));

                        Log.v(null,answer.toString());
                        name_view.setText(answer.getString("name"));
                        place_view.setText("Place:    lat "+answer.getString("latitude")+"\n long "+answer.getString("longitude"));
                        time_view.setText("Time: "+answer.getString("action_time"));
                        description_view.setText(answer.getString("description"));
                        chat=answer.getJSONObject("chat").getString("chat_id");
                        JSONArray messages = answer.getJSONObject("chat").getJSONArray("messages");

                        JSONArray users_json= answer.getJSONArray("users");
                        String[] users= new String[users_json.length()];
                        is_member = false;
                        for (int i=0;i<users_json.length();i++){
                                if (users_json.getJSONObject(i).getString("user_id")==user_id){
                                    is_member=true;
                                }
                        }
                        if (is_member){
                            message_view.setEnabled(true);
                            send_button.setText("Send");
                        } else{
                            message_view.setEnabled(false);
                            send_button.setText("Join");
                        }

                        action_id = answer.getString("action_id");



                        LayoutInflater inflater = getLayoutInflater();

                        for (int i=0;i<messages.length();i++){
                            JSONObject item = messages.getJSONObject(i);

                            View new_view = inflater.inflate(R.layout.message,layout);

                            CardView card_view =(CardView) layout.getChildAt(i);
                            card_view.setTag(item.getString("from_user"));

                            String from_user = item.getString("from_user");
                            String sender_name = "Deleted user";
                            for (int j=0;j<users_json.length();j++){
                                JSONObject user = users_json.getJSONObject(j);
                                if (user.getString("user_id")==from_user){
                                    sender_name=user.getString("first_name")+" "+user.getString("second_name");
                                }
                            }

                            TextView name_view1 = (TextView)   ((CardView)card_view).getChildAt(0);
                            name_view1.setText(sender_name);



                            TextView description_view1 = (TextView)   ((CardView)card_view).getChildAt(1);
                            description_view1.setText(item.getString("message"));
                        }


                    } else{
                        //goto_events(null);
                        description_view.setText(answer.toString());
                    }
                } catch (JSONException | ExecutionException | InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        ((MigraNet)this.getApplication()).setChat(chat);
        scroll_view.postDelayed(new Runnable() {
            @Override
            public void run() {
                scroll_view.fullScroll(ScrollView.FOCUS_DOWN);
            }
        }, 100);
    }

    public void goto_events(View view){
        Intent intent = new Intent(EventInfoActivity.this, EventsActivity.class);
        startActivity(intent);
    }

}