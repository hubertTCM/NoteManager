package com.hubert.notesmanager.ui.yiAn;

import java.util.*;

import android.content.Context;

import com.hubert.notesmanager.dal.DatabaseHelper;
import com.hubert.notesmanager.dal.orm.*;

public class YiAnDetailModel {
    private DatabaseHelper mDbHelper;
    private List<YiAnPrescriptionModel> mItems;
    private YiAnDetailEntity mEntity;
    
    public YiAnDetailModel(YiAnDetailEntity entity, DatabaseHelper dbHelper){
        mEntity = entity;
        mDbHelper = dbHelper;
    }
    
    public YiAnDetailEntity getEntity(){
        return mEntity;
    }
    
    public List<YiAnPrescriptionModel> getPrescriptions(){
        if (mItems != null){
            return mItems;
        }
        mItems = new Vector<YiAnPrescriptionModel>();
        YiAnPrescriptionDao dao = new YiAnPrescriptionDao(mDbHelper.getReadableDatabase()); 
        for (YiAnPrescriptionEntity prescription : dao.loadByYiAnDetailId(mEntity.getId())){
            mItems.add(new YiAnPrescriptionModel(prescription, mDbHelper));
        }
        
        return mItems;
    }
}
