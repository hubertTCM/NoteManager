package com.hubert.tcm.yian.ui;

import java.util.List;

import com.hubert.tcm.dal.DatabaseHelper;
import com.hubert.tcm.dal.orm.*;

public class YiAnPrescriptionModel {
    private DatabaseHelper mDbHelper;
    private YiAnPrescriptionEntity mEntity;
    
    public YiAnPrescriptionModel (YiAnPrescriptionEntity entity, DatabaseHelper dbHelper){
        mDbHelper = dbHelper;
        mEntity = entity;
    }
    
    public YiAnPrescriptionEntity getEntity(){
        return mEntity;
    }
    
    public List<YiAnCompositionEntity> getCompositions(){
        YiAnCompositionDao dao = new YiAnCompositionDao(mDbHelper.getReadableDatabase());
        return dao.loadByPrescriptionId(mEntity.getId());
    }
}
