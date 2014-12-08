package com.neterra.example;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;
import android.widget.TextView;
import de.greenrobot.event.EventBus;

public class MainActivity extends Activity {
	
	TextView text1;
	EventBus mEventBus = EventBus.getDefault();
    
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
	}
	
	@Override
	protected void onStart() {
		super.onStart();
		if(!mEventBus.isRegistered(this)) {
			mEventBus.register(this);
		}
	}
	
	@Override
	protected void onDestroy() {
		super.onDestroy();
		mEventBus.unregister(this);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.activity_main, menu);
		text1 = (TextView)findViewById(R.id.textView1);
		
		return true;
	}

	public void onButton1Click(View v) {
		mEventBus.post((String)"Message!!!");
		mEventBus.post(new Events.FirstEvent());
		EventBus.getDefault().post(new Events.SecondEvent());
    }

	public void onEvent(String msg) 
	{
		text1.setText(msg);
	}
	
	public void onEvent(Events.FirstEvent e) 
	{
		text1.append(" - FirstEvent");
	}
	
	public void onEvent(Events.SecondEvent e) 
	{
		text1.append(" - SecondEvent");
	}

	public void onEventMainThread(Events.SecondEvent e) 
	{
		text1.append(" - SecondEvent");
	}

    public void onEventBackgroundThread(Events.SecondEvent e) 
	{
		text1.append(" - SecondEvent");
	}

    public void onEventAsync(Events.SecondEvent e) 
	{
		text1.append(" - SecondEvent");
	}

	public static class Events {
		public static class FirstEvent {
		}
		public static class SecondEvent {
		}
	}
}
