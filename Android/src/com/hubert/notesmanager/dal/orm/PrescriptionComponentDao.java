package com.hubert.notesmanager.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class PrescriptionComponentDao {

	private String mIdColumnName = "_id";
	private String mPrescriptionColumnName = "prescription_id";
	private String mComponentColumnName = "component";
	private String mUnitColumnName = "unit_id";
	private String mQuantityColumnName = "quantity";
	private String mCommentColumnName = "comment";
	
	private SQLiteDatabase mDatabase;

	public PrescriptionComponentDao(SQLiteDatabase database) {
		mDatabase = database;
	}

	public List<PrescriptionComponentEntity> loadAll() {
		Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptioncomponent", null);
		return loadAll(cursor);
	}
	private List<PrescriptionComponentEntity> loadAll(Cursor cursor) {
		Vector<PrescriptionComponentEntity> items = new Vector<PrescriptionComponentEntity>();
		for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
			items.add(createEntity(cursor));
		}
		return items;
	}

	public PrescriptionComponentEntity load(long id) {
		String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
		Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptioncomponent where _id = ?", whereArgs);
		return createEntity(cursor);
	}

	private PrescriptionComponentEntity createEntity(Cursor cursor) {
		int columnIndex = 0;
	
		columnIndex = cursor.getColumnIndex(mIdColumnName);
		long idValue = cursor.getLong(columnIndex);
		PrescriptionComponentEntity entity = new PrescriptionComponentEntity(idValue);
	
		columnIndex = cursor.getColumnIndex(mPrescriptionColumnName);
		long prescriptionValue = cursor.getLong(columnIndex);
		entity.setPrescription(prescriptionValue);
	
		columnIndex = cursor.getColumnIndex(mComponentColumnName);
		String componentValue = cursor.getString(columnIndex);
		entity.setComponent(componentValue);
	
		columnIndex = cursor.getColumnIndex(mUnitColumnName);
		String unitValue = cursor.getString(columnIndex);
		entity.setUnit(unitValue);
	
		columnIndex = cursor.getColumnIndex(mQuantityColumnName);
		double quantityValue = cursor.getDouble(columnIndex);
		entity.setQuantity(quantityValue);
	
		columnIndex = cursor.getColumnIndex(mCommentColumnName);
		String commentValue = cursor.getString(columnIndex);
		entity.setComment(commentValue);
	
		return entity;
	}
}
