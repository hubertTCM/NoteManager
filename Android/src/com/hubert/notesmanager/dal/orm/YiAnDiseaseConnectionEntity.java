package com.hubert.notesmanager.dal.orm;

public class YiAnDiseaseConnectionEntity {
    private long mId;
    private long mYiAnId;
    private String mDiseaseId;

    public YiAnDiseaseConnectionEntity( long id ) {
        mId = id;
    }

    public long getId() {
        return mId;
    }
    
    public long getYiAnId() {
        return mYiAnId;
    }
    
    public void setYiAnId(long value) {
        mYiAnId = value;
    }
    
    public String getDiseaseId() {
        return mDiseaseId;
    }
    
    public void setDiseaseId(String value) {
        mDiseaseId = value;
    }
    
}
