package com.hubert.tcm.dal.orm;

public class PrescriptionEntity {
    private long mId;
    private String mName;
    private String mAllHerbText;
    private long mComeFromId;
    private String mComment;

    public PrescriptionEntity( long id ) {
        mId = id;
    }

    public long getId() {
        return mId;
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
    
    public long getComeFromId() {
        return mComeFromId;
    }
    
    public void setComeFromId(long value) {
        mComeFromId = value;
    }
    
    public String getComment() {
        return mComment;
    }
    
    public void setComment(String value) {
        mComment = value;
    }
    
}
