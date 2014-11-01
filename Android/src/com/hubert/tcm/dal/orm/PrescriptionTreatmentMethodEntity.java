package com.hubert.tcm.dal.orm;

public class PrescriptionTreatmentMethodEntity {
    private long mId;
    private String mMethodId;
    private long mPrescriptionId;

    public PrescriptionTreatmentMethodEntity( long id ) {
        mId = id;
    }

    public long getId() {
        return mId;
    }
    
    public String getMethodId() {
        return mMethodId;
    }
    
    public void setMethodId(String value) {
        mMethodId = value;
    }
    
    public long getPrescriptionId() {
        return mPrescriptionId;
    }
    
    public void setPrescriptionId(long value) {
        mPrescriptionId = value;
    }
    
}
