package com.example.a0403;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.loopj.android.http.AsyncHttpClient;
import com.loopj.android.http.AsyncHttpResponseHandler;
import com.loopj.android.http.RequestParams;


import org.json.JSONException;
import org.json.JSONObject;



import java.util.Timer;
import java.util.TimerTask;

import cz.msebera.android.httpclient.Header;
import cz.msebera.android.httpclient.HttpResponse;
import cz.msebera.android.httpclient.client.ResponseHandler;

import static android.widget.Toast.LENGTH_SHORT;
import static android.widget.Toast.makeText;


public class MainActivity extends AppCompatActivity {
    TextView humidity;
    TextView temperature;
    TextView light;
    TextView noise;
    AsyncHttpClient client;
    Button buttonforstate;
    AsyncHttpResponseHandler msgforstate;
    Button buttonforlight;
    EditText col;
    EditText row;
    //AsyncHttpResponseHandler msgforlight;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        humidity = findViewById(R.id.humidity);
        temperature = findViewById(R.id.temperature);
        light = findViewById(R.id.light);
        noise = findViewById(R.id.noise);
        buttonforstate = findViewById(R.id.buttonforstate);
        buttonforlight = findViewById(R.id.buttonforlight);
        col = findViewById(R.id.col);
        row = findViewById(R.id.row);


        client = new AsyncHttpClient();
        client.setConnectTimeout(4000);

        msgforstate = new AsyncHttpResponseHandler() {
            @Override
            public void onSuccess(int statusCode, Header[] headers, byte[] responseBody) {
                String str = new String(responseBody);
                //Toast.makeText(getApplicationContext(),str, Toast.LENGTH_LONG).show();
                //humidity.setText(str);

                try {
                    JSONObject jobj = new JSONObject(str);
                    humidity.setText(jobj.getString("humidity"));
                    temperature.setText(jobj.getString("temperature"));
                    light.setText(jobj.getString("light"));
                    noise.setText(jobj.getString("noise"));
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void onFailure(int statusCode, Header[] headers, byte[] responseBody, Throwable error) {
                Toast.makeText(getApplicationContext(), "is the server awake?" , Toast.LENGTH_LONG).show();
            }
        };

        client.get("http://192.168.0.58:5000/update", msgforstate);

        buttonforstate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                client.get("http://192.168.0.58:5000/update", msgforstate);
            }
        });


        // client.post(url, params, responsehandler)
        buttonforlight.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                AsyncHttpResponseHandler msgforlight = new AsyncHttpResponseHandler() {
                    @Override
                    public void onSuccess(int statusCode, Header[] headers, byte[] responseBody) {
                        col.setText("");
                        row.setText("");
                        Toast.makeText(getApplicationContext(), "Success" , LENGTH_SHORT).show();
                    }

                    @Override
                    public void onFailure(int statusCode, Header[] headers, byte[] responseBody, Throwable error) {
                        col.setText("");
                        row.setText("");
                        Toast.makeText(getApplicationContext(), "Failure" , LENGTH_SHORT).show();
                    }
                };

                String _col = new String(col.getText().toString());
                String _row = new String(row.getText().toString());

                /*
                RequestParams params = new RequestParams();
                params.put("col", _col);
                params.put("row", _row);
                client.post("http://192.168.0.58:5000/input", params, msgforlight);
                */

                if (Integer.parseInt(_col) == 0 && Integer.parseInt(_row) == 0) {
                    RequestParams params = new RequestParams();
                    params.put("col", _col);
                    params.put("row", _row);
                    client.post("http://192.168.0.58:5000/input", params, msgforlight);
                }else if (Integer.parseInt(_col) > 4 || Integer.parseInt(_col) < 1){
                    Toast.makeText(getApplicationContext(), "column should be from 1 to 4" , LENGTH_SHORT).show();
                }else if (Integer.parseInt(_row) > 6 || Integer.parseInt(_row) < 1){
                    Toast.makeText(getApplicationContext(), "column should be from 1 to 4" , LENGTH_SHORT).show();
                }else{
                    RequestParams params = new RequestParams();
                    params.put("col", _col);
                    params.put("row", _row);
                    client.post("http://192.168.0.58:5000/input", params, msgforlight);

                }
            }
        });

    }

}
