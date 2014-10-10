package com.hubert.notesmanager.dal.orm;

public class PrescriptionEntity {
	private long mId;
	private String mName;
	private String mAllHerbText;
	private long mComeFrom;
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
	
	public long getComeFrom() {
		return mComeFrom;
	}
	
	public void setComeFrom(long value) {
		mComeFrom = value;
	}
	
	public String getComment() {
		return mComment;
	}
	
	public void setComment(String value) {
		mComment = value;
	}
	
}
