package com.hubert.tcm.yian.ui;

import java.util.*;

import com.hubert.tcm.R;
import com.hubert.tcm.dal.DatabaseHelper;
import com.hubert.tcm.dal.orm.*;
import android.app.Activity;
import android.content.*;
import android.os.Bundle;
import android.view.*;
import android.view.View.OnClickListener;
import android.widget.*;

public class YiAnSummaryActivity extends Activity{
    public YiAnSummaryActivity(){
    }
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_yian_summary);
        
        setUp();
    }
    
    private  void setUp(){
        ListView listView = (ListView)findViewById(R.id.listview_yian);
        DatabaseHelper dbHelper = new DatabaseHelper(this);
        YiAnDetailDao dao = new YiAnDetailDao(dbHelper.getReadableDatabase());
        Vector<YiAnSummaryViewModel> models = new Vector<YiAnSummaryViewModel>();
        for (YiAnDetailEntity entity : dao.loadFirst()){
            models.add(new YiAnSummaryViewModel(dbHelper, entity));
        }
        ArrayAdapter<YiAnSummaryViewModel> adapter = new ArrayAdapter<YiAnSummaryViewModel>(this,android.R.layout.simple_list_item_2, models){
            @Override
            public View getView(int position, View convertView, ViewGroup parent){
                TwoLineListItem item;
                if(convertView == null){
                    LayoutInflater inflater = LayoutInflater.from(YiAnSummaryActivity.this);
                    item = (TwoLineListItem)inflater.inflate(android.R.layout.simple_list_item_2, null);
                    item.getText2().setOnClickListener(new OnClickListener(){
                        @Override
                        public void onClick(View paramView){
                            YiAnSummaryViewModel summaryModel = (YiAnSummaryViewModel)paramView.getTag();
                            YiAnDetailEntity entity = summaryModel.getEntity();
                            Intent intent = new Intent(YiAnSummaryActivity.this, YiAnDetailActivity.class);
                            intent.putExtra(YiAnDetailActivity.YIAN_ID, entity.getYiAnId());
                            intent.putExtra(YiAnDetailActivity.YIAN_NAME, summaryModel.getName());
                            YiAnSummaryActivity.this.startActivity(intent);
                        }
                    });
                }else{
                    item = (TwoLineListItem)convertView;
                }
                YiAnSummaryViewModel data = getItem(position);
                item.getText1().setText(data.getName());
                item.getText2().setText(data.getSummary());
                item.getText2().setTag(data);
                return item;
            }
        };
        listView.setAdapter(adapter);
    }
}
