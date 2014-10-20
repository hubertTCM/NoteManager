package com.hubert.notesmanager.ui.yiAn;


import java.util.*;

import com.hubert.notesmanager.R;
import com.hubert.notesmanager.dal.DatabaseHelper;
import com.hubert.notesmanager.dal.orm.*;
import com.hubert.notesmanager.ui.prescription.PrescriptionActivity;
import com.hubert.notesmanager.ui.prescription.PrescritionDetailViewModel;
import com.hubert.notesmanager.util.Util;

import android.app.ActionBar.LayoutParams;
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
    
    private LinearLayout mLinearLayoutDetailsRoot;
    
    private YiAnModel mYiAnModel;
    private List<YiAnDetailModel> mDetails;
    private int mCurrentOrder;
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_yian_detail);
        
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
        mLinearLayoutDetailsRoot = (LinearLayout)findViewById(R.id.yian_details);
        
        showDescription();
    }
    
    private void showDescription(){
        YiAnDetailModel detailModel = mDetails.get(mCurrentOrder);
        YiAnDetailEntity entity = detailModel.getEntity();
        createTextView(entity.getDescription(), mLinearLayoutDetailsRoot);

        if (detailModel.getPrescriptions().size() > 0){
            createButton(mLinearLayoutDetailsRoot);
        }
    }
    
    private void showPrescriptions(){
//        Toast t = Toast.makeText(this, "show prescription", 1);
//        t.show();

        YiAnDetailModel detailModel = mDetails.get(mCurrentOrder);
        for (YiAnPrescriptionModel prescription : detailModel.getPrescriptions()){
            showPrescription(prescription);
        }

        createTextView(detailModel.getEntity().getComments(), mLinearLayoutDetailsRoot);
        
        mCurrentOrder += 1;
        if (mCurrentOrder < mDetails.size()){
            showDescription();
        }
        
    }
    
    private void showPrescription(YiAnPrescriptionModel prescription){
       YiAnPrescriptionEntity prescriptionEntity = prescription.getEntity();
       String name = prescriptionEntity.getName();
       if (!Util.isNullOrEmpty(name)){
           createTextView(name, mLinearLayoutDetailsRoot);
       }
       
       String text = " ";
       for (YiAnCompositionEntity item : prescription.getCompositions()){
           text += " " + item.getComponent();
           if (item.getQuantity() > 0){
               text += Double.toString(item.getQuantity());
           }
           if (!Util.isNullOrEmpty(item.getUnitId())){
               text += item.getUnitId();
           }
           if (!Util.isNullOrEmpty(item.getComment())){
               text += item.getComment();
           }
       }
       
       if (prescriptionEntity.getQuantity() > 0){
           text += " " + Double.toString(prescriptionEntity.getQuantity());
       }
       if (!Util.isNullOrEmpty(prescriptionEntity.getUnit())){
           text += prescriptionEntity.getUnit();
       }
       
       if (!Util.isNullOrEmpty(prescriptionEntity.getComment())){
           text += "\n" + prescriptionEntity.getComment();
       }
       createTextView(text, mLinearLayoutDetailsRoot);
    }
    
    private void createTextView(String text, ViewGroup parent){
        if (Util.isNullOrEmpty(text)){
            return;
        }
        TextView txtView = new TextView(this);
        txtView.setLayoutParams(new LayoutParams(
                LayoutParams.FILL_PARENT,
                LayoutParams.WRAP_CONTENT));
        txtView.setText(text);
        parent.addView(txtView);
    }
    
    private void createButton (ViewGroup parent){
        Button b = new Button(this);
        b.setText("show prescription");
        b.setOnClickListener(new OnClickListener(){
            
            @Override
            public void onClick(View paramView){
                showPrescriptions();
                mLinearLayoutDetailsRoot.removeView(paramView);
            }
        });
        
        parent.addView(b);
    }
}
