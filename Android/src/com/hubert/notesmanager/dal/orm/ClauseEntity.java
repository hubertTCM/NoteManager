package com.hubert.notesmanager.dal.orm;

public class ClauseEntity {
    private long mId;
    private long mComeFromId;
    private long mIndex;
    private String mContent;

    public ClauseEntity( long id ) {
        mId = id;
    }

    public long getId() {
        return mId;
    }
    
    public long getComeFromId() {
        return mComeFromId;
    }
    
    public void setComeFromId(long value) {
        mComeFromId = value;
    }
    
    public long getIndex() {
        return mIndex;
    }
    
    public void setIndex(long value) {
        mIndex = value;
    }
    
    public String getContent() {
        return mContent;
    }
    
    public void setContent(String value) {
        mContent = value;
    }
    
}
