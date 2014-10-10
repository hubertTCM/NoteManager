package com.hubert.notesmanager.dal.orm;

public class ClauseEntity {
	private long mId;
	private long mComeFrom;
	private long mIndex;
	private String mContent;

	public ClauseEntity( long id ) {
		mId = id;
	}

	public long getId() {
		return mId;
	}
	
	public long getComeFrom() {
		return mComeFrom;
	}
	
	public void setComeFrom(long value) {
		mComeFrom = value;
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
