package com.hubert.tcm.yian.ui;


import java.util.*;

import com.hubert.tcm.R;
import com.hubert.tcm.dal.orm.*;
import com.hubert.tcm.util.Util;

import android.app.Activity;
import android.content.*;
import android.os.Bundle;
import android.view.*;
import android.view.View.OnClickListener;
import android.widget.*;

public class YiAnDetailActivity extends Activity{
    
    public final static String YIAN_ID = "yiAnId";
    public final static String YIAN_NAME = "yiAnName";
    
    private long mYiAnId;
    
    private LinearLayout mLayoutDetails;
    private LayoutInflater mInflater;
    
    private YiAnModel mYiAnModel;
    private List<YiAnDetailModel> mDetails;
    private int mCurrentOrder;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_yian_detail);
        
        mInflater = LayoutInflater.from(this);
        
        Intent intent = getIntent();
        mYiAnId = intent.getLongExtra(YiAnDetailActivity.YIAN_ID, 0);
        mYiAnModel = new YiAnModel(mYiAnId, this);
        mDetails = mYiAnModel.getDetails();
    
        String name = intent.getStringExtra(YiAnDetailActivity.YIAN_NAME);
        if (name == null){
            name = "";
        }
        
        TextView textView = (TextView)findViewById(R.id.yian_name);
        textView.setText(name);
        mLayoutDetails = (LinearLayout)findViewById(R.id.yian_details);
        
        showDescription();
    }
    
    private void showDescription(){
        YiAnDetailModel detailModel = mDetails.get(mCurrentOrder);
        YiAnDetailEntity entity = detailModel.getEntity();
        createTextView(entity.getDescription(), mLayoutDetails);

        if (detailModel.getPrescriptions().size() > 0){
            createButton(mLayoutDetails);
        }
    }
    
    private void showPrescriptions(){
//        Toast t = Toast.makeText(this, "show prescription", 1);
//        t.show();

        YiAnDetailModel detailModel = mDetails.get(mCurrentOrder);
        for (YiAnPrescriptionModel prescription : detailModel.getPrescriptions()){
            showSinglePrescription(prescription);
        }

        createTextView(detailModel.getEntity().getComments(), mLayoutDetails);
        
        mCurrentOrder += 1;
        if (mCurrentOrder < mDetails.size()){
            showDescription();
        }
    }
    
    private void showSinglePrescription(YiAnPrescriptionModel prescription){
       PrescriptionViewModel viewModel = new PrescriptionViewModel(mInflater, prescription);
       viewModel.createUI(mLayoutDetails);
    }
    
    private TextView createTextView(String text, ViewGroup parent){
        if (Util.isNullOrEmpty(text)){
            return null;
        }
        mInflater.inflate(R.layout.textview_description, parent);
        TextView txtView = (TextView)parent.getChildAt(parent.getChildCount() - 1);
        txtView.setText(text);
        return txtView;
    }
    
    private void createButton (ViewGroup parent){
        mInflater.inflate(R.layout.btn_show_prescription, parent);
        Button btn = (Button)parent.getChildAt(parent.getChildCount() - 1);
        btn.setOnClickListener(new OnClickListener(){
            @Override
            public void onClick(View paramView){
                showPrescriptions();
                mLayoutDetails.removeView(paramView);
            }
        });
    }
}
