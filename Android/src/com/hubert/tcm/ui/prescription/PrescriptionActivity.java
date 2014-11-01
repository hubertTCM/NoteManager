package com.hubert.tcm.ui.prescription;

import com.hubert.tcm.R;
import com.hubert.tcm.dal.DatabaseHelper;
import com.hubert.tcm.dal.orm.*;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.*;

public class PrescriptionActivity extends Activity{
    
    public final static String PRESCRIPTION_ID = "prescriptionId";
    private PrescritionDetailViewModel mDetailViewModel;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_prescription);
        
        Intent intent = getIntent();
        long prescriptionId = intent.getLongExtra(PrescriptionActivity.PRESCRIPTION_ID, 0);
        
        
        mDetailViewModel = new PrescritionDetailViewModel(prescriptionId, this);
        
        TextView textViewPrescriptionName = (TextView)findViewById(R.id.prescritiption_name);
        textViewPrescriptionName.setText(mDetailViewModel.getName());
        
        ListView listViewComponent = (ListView)findViewById(R.id.prescription_components);
        listViewComponent.setAdapter(mDetailViewModel.getComponentAdapter());
        

        ListView listViewClauses = (ListView)findViewById(R.id.prescription_clauses);
        listViewClauses.setAdapter(mDetailViewModel.getCluaseAdapter());
    }

}
