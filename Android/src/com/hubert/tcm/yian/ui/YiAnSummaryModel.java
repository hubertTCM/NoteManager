package com.hubert.tcm.yian.ui;

import java.util.*;

import com.hubert.tcm.dal.DatabaseHelper;
import com.hubert.tcm.dal.orm.*;

public class YiAnSummaryModel {

    private YiAnDetailEntity mEntity;
    private DatabaseHelper mDbHelper;
    
    private String mName = "";
    private String mSummary = "";
    
    public YiAnSummaryModel(DatabaseHelper dbHelper, YiAnDetailEntity entity){
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
    
    public YiAnDetailEntity getEntity(){
        return mEntity;
    }
}
