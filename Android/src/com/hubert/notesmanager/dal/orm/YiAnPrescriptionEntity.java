package com.hubert.notesmanager.dal.orm;

public class YiAnPrescriptionEntity {
    private long mId;
    private long mYiAnDetailId;
    private String mName;
    private String mAllHerbText;
    private String mUnit;
    private double mQuantity;
    private String mComment;

    public YiAnPrescriptionEntity( long id ) {
        mId = id;
    }

    public long getId() {
        return mId;
    }
    
    public long getYiAnDetailId() {
        return mYiAnDetailId;
    }
    
    public void setYiAnDetailId(long value) {
        mYiAnDetailId = value;
    }
    
    public String getName() {
        return mName;
    }
    
    public void setName(String value) {
        mName = value;
    }
    
    public String getAllHerbText() {
        return mAllHerbText;
    }
    
    public void setAllHerbText(String value) {
        mAllHerbText = value;
    }
    
    public String getUnit() {
        return mUnit;
    }
    
    public void setUnit(String value) {
        mUnit = value;
    }
    
    public double getQuantity() {
        return mQuantity;
    }
    
    public void setQuantity(double value) {
        mQuantity = value;
    }
    
    public String getComment() {
        return mComment;
    }
    
    public void setComment(String value) {
        mComment = value;
    }
    
}
