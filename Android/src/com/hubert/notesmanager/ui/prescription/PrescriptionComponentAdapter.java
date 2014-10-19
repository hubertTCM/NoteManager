package com.hubert.notesmanager.ui.prescription;

import java.util.List;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.*;

import com.hubert.notesmanager.R;
import com.hubert.notesmanager.dal.orm.*;
import com.hubert.notesmanager.ui.main.ClauseViewModel;

public class PrescriptionComponentAdapter extends ArrayAdapter<PrescriptionComponentEntity>{
    private LayoutInflater mInflater;
    private Context mContext;

    public PrescriptionComponentAdapter(Context context,
            int textViewResourceId, List<PrescriptionComponentEntity> components) {
        super(context, textViewResourceId, components);
        
        mContext = context;
        mInflater = LayoutInflater.from(mContext);
    }
    

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        PrescriptionComponentEntity item = getItem(position);

        if(convertView == null){
            convertView = mInflater.inflate(R.layout.prescription_component, null);
        }
        Button btnHerb = (Button) convertView.findViewById(R.id.herb_name); 
        btnHerb.setText(item.getComponent());
        
        TextView txtViewQuantity = (TextView)convertView.findViewById(R.id.quantity);
        txtViewQuantity.setText(Double.toString(item.getQuantity()));
       
        TextView txtViewUnit = (TextView)convertView.findViewById(R.id.unit);
        txtViewUnit.setText(item.getUnitId());
        
        TextView txtComment = (TextView)convertView.findViewById(R.id.comment);
        txtComment.setText(item.getComment());

        return convertView;
    }


}
