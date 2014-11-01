package com.hubert.tcm.dal.orm;

public class YiAnDetailEntity {
    private long mId;
    private long mOrder;
    private long mYiAnId;
    private String mDescription;
    private String mComments;
    private long mComeFromId;

    public YiAnDetailEntity( long id ) {
        mId = id;
    }

    public long getId() {
        return mId;
    }
    
    public long getOrder() {
        return mOrder;
    }
    
    public void setOrder(long value) {
        mOrder = value;
    }
    
    public long getYiAnId() {
        return mYiAnId;
    }
    
    public void setYiAnId(long value) {
        mYiAnId = value;
    }
    
    public String getDescription() {
        return mDescription;
    }
    
    public void setDescription(String value) {
        mDescription = value;
    }
    
    public String getComments() {
        return mComments;
    }
    
    public void setComments(String value) {
        mComments = value;
    }
    
    public long getComeFromId() {
        return mComeFromId;
    }
    
    public void setComeFromId(long value) {
        mComeFromId = value;
    }
    
}
