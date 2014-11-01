package com.hubert.tcm.dal.orm;

public class PrescriptionClauseConnectionEntity {
    private long mId;
    private long mClauseId;
    private long mPrescriptionId;

    public PrescriptionClauseConnectionEntity( long id ) {
        mId = id;
    }

    public long getId() {
        return mId;
    }
    
    public long getClauseId() {
        return mClauseId;
    }
    
    public void setClauseId(long value) {
        mClauseId = value;
    }
    
    public long getPrescriptionId() {
        return mPrescriptionId;
    }
    
    public void setPrescriptionId(long value) {
        mPrescriptionId = value;
    }
    
}
