package com.hubert.notesmanager.ui.yiAn;

import java.util.*;

import com.hubert.notesmanager.dal.DatabaseHelper;
import com.hubert.notesmanager.dal.orm.*;

public class YiAnSummaryViewModel {

    private YiAnDetailEntity mEntity;
    private DatabaseHelper mDbHelper;
    
    private String mName = "";
    private String mSummary = "";
    
    public YiAnSummaryViewModel(DatabaseHelper dbHelper, YiAnDetailEntity entity){
        mDbHelper = dbHelper;
        mEntity = entity;
    }
    
    public String getName(){
        if (!mName.isEmpty()){
            return mName;
        }
        YiAnDiseaseConnectionDao dao = new YiAnDiseaseConnectionDao(mDbHelper.getReadableDatabase());
        List<YiAnDiseaseConnectionEntity> items = dao.loadByYiAnId(mEntity.getId());
        for (YiAnDiseaseConnectionEntity item : items){
            mName += item.getDiseaseId() + "、";
        }
        mName = mName.substring(0, mName.length() - 1);
        return mName;
    }
    
    public String getSummary(){
        if (!mSummary.isEmpty()){
            return mSummary;
        }
        mSummary = mEntity.getDescription();
        if (mSummary.length() > 100){
            mSummary = mSummary.substring(0, 100) + "...";
        }
        return mSummary;
    }
    
    public long getId(){
        return mEntity.getId();
    }
}
