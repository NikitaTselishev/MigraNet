package com.example.migranet;

import android.app.Application;

public class MigraNet extends Application {

    private String session;
    private String chosen_event;
    private String chosen_chat;
    private String user_id;

    public String getUserId(){
        return user_id;
    }
    public void setUserId(String value){
        user_id = value;
    }

    public String getChat(){
        return chosen_chat;
    }
    public void setChat(String value){
        chosen_chat = value;
    }

    public String getEvent(){
        return chosen_event;
    }
    public void setEvent(String value){
        chosen_event = value;
    }

    public String getSession(){
        return session;
    }

    public void setSession(String value){
        session = value;
    }
}
