package com.hubert.notesmanager.dal.orm;

public class YiAnCompositionEntity {
    private long mId;
    private long mPrescriptionId;
    private String mComponent;
    private String mUnitId;
    private double mQuantity;
    private String mComment;

    public YiAnCompositionEntity( long id ) {
        mId = id;
    }

    public long getId() {
        return mId;
    }
    
    public long getPrescriptionId() {
        return mPrescriptionId;
    }
    
    public void setPrescriptionId(long value) {
        mPrescriptionId = value;
    }
    
    public String getComponent() {
        return mComponent;
    }
    
    public void setComponent(String value) {
        mComponent = value;
    }
    
    public String getUnitId() {
        return mUnitId;
    }
    
    public void setUnitId(String value) {
        mUnitId = value;
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
