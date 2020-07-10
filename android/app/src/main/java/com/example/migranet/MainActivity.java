package com.example.migranet;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    public static String session;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        session = ((MigraNet) this.getApplication()).getSession();


    }

    public void goto_events(View view){
        Intent intent = new Intent(MainActivity.this, EventsActivity.class);
        startActivity(intent);
    }
}