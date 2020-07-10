package com.example.migranet;

import android.app.Application;

public class MigraNet extends Application {

    private String session;
    private String chosen_event;

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
