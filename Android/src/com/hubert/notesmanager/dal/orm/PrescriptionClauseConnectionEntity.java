package com.hubert.notesmanager.dal.orm;

public class PrescriptionClauseConnectionEntity {
	private long mId;
	private long mClause;
	private long mPrescription;

	public PrescriptionClauseConnectionEntity( long id ) {
		mId = id;
	}

	public long getId() {
		return mId;
	}
	
	public long getClause() {
		return mClause;
	}
	
	public void setClause(long value) {
		mClause = value;
	}
	
	public long getPrescription() {
		return mPrescription;
	}
	
	public void setPrescription(long value) {
		mPrescription = value;
	}
	
}
