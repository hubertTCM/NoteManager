package com.hubert.notesmanager.dal.orm;

public class PrescriptionComponentEntity {
	private long mId;
	private long mPrescription;
	private String mComponent;
	private String mUnit;
	private double mQuantity;
	private String mComment;

	public PrescriptionComponentEntity( long id ) {
		mId = id;
	}

	public long getId() {
		return mId;
	}
	
	public long getPrescription() {
		return mPrescription;
	}
	
	public void setPrescription(long value) {
		mPrescription = value;
	}
	
	public String getComponent() {
		return mComponent;
	}
	
	public void setComponent(String value) {
		mComponent = value;
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
