package com.hubert.tcm.yian.ui;


import android.view.*;
import android.widget.*;

import com.hubert.tcm.R;
import com.hubert.tcm.dal.orm.*;
import com.hubert.tcm.util.*;

public class PrescriptionViewModel {
    private LayoutInflater mInflater;
    private YiAnPrescriptionModel mData;
    public PrescriptionViewModel(LayoutInflater inflater, YiAnPrescriptionModel data){
        mInflater = inflater;
        mData = data;
    }

    public View createUI(ViewGroup parent){
        LinearLayout root = (LinearLayout)mInflater.inflate(R.layout.linearlayout_yian_prescription, parent);
        if (parent != null){
            root = (LinearLayout) Util.getLastChild(parent);
        }
        
        YiAnPrescriptionEntity entity = mData.getEntity();
        String name = entity.getName();
        updateTextView(R.id.name, name, root);
        
        ViewGroup compositionContainer = (ViewGroup) root.findViewById(R.id.composition_container);
        for (YiAnCompositionEntity composition : mData.getCompositions()){
            createComposition(composition, compositionContainer);
        }
        
        String text = "";
        double quantity = entity.getQuantity();
        if (quantity > 0){
            text += Util.convert(quantity);
        }
        if (!Util.isNullOrEmpty(entity.getUnit())){
            text += entity.getUnit();
        }
        if (!Util.isNullOrEmpty(entity.getComment())){
            text += "\n" + entity.getComment();
        }
        updateTextView(R.id.other, text, root);
        return root;
    }

    private void updateTextView(int resource, String text, ViewGroup root) {
        TextView textView = (TextView)root.findViewById(resource);
        if (!Util.isNullOrEmpty(text)){
            textView.setText(text);
        }
        else{
            root.removeView(textView);
        }
    }
    
    private View inflate(int resource, ViewGroup root){
        View ui = mInflater.inflate(resource, root);
        
        if (root != null){
            return Util.getLastChild(root);
        }
        
        return ui;
    }
    
    private void createComposition(YiAnCompositionEntity entity, ViewGroup container){
        TextView textViewName = (TextView)inflate(R.layout.textview_herb, container);
        textViewName.setText(entity.getComponent());
        String text = "";
        double quantity = entity.getQuantity();
        if (quantity > 0){
            text += Util.convert(quantity);
        }
        if (!Util.isNullOrEmpty(entity.getUnitId())){
            text += entity.getUnitId();
        }
        if (!Util.isNullOrEmpty(entity.getComment())){
            text += "(" + entity.getComment() + ")";
        }
        TextView textViewOther = (TextView)inflate(R.layout.textview_description, container);
        textViewOther.setText(text);
    }
}
