package com.hubert.notesmanager.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class PrescriptionClauseConnectionDao {

	private String mIdColumnName = "_id";
	private String mClauseColumnName = "clause_id";
	private String mPrescriptionColumnName = "prescription_id";
	
	private SQLiteDatabase mDatabase;

	public PrescriptionClauseConnectionDao(SQLiteDatabase database) {
		mDatabase = database;
	}

	public List<PrescriptionClauseConnectionEntity> loadAll() {
		Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptionclauseconnection", null);
		return loadAll(cursor);
	}
	private List<PrescriptionClauseConnectionEntity> loadAll(Cursor cursor) {
		Vector<PrescriptionClauseConnectionEntity> items = new Vector<PrescriptionClauseConnectionEntity>();
		for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
			items.add(createEntity(cursor));
		}
		return items;
	}

	public PrescriptionClauseConnectionEntity load(long id) {
		String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
		Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptionclauseconnection where _id = ?", whereArgs);
		return createEntity(cursor);
	}
	
	public List<PrescriptionClauseConnectionEntity> loadByClause(long id) {
		String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
		Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptionclauseconnection where clause_id = ?", whereArgs);
		return loadAll(cursor);
	}

	private PrescriptionClauseConnectionEntity createEntity(Cursor cursor) {
		int columnIndex = 0;
	
		columnIndex = cursor.getColumnIndex(mIdColumnName);
		long idValue = cursor.getLong(columnIndex);
		PrescriptionClauseConnectionEntity entity = new PrescriptionClauseConnectionEntity(idValue);
	
		columnIndex = cursor.getColumnIndex(mClauseColumnName);
		long clauseValue = cursor.getLong(columnIndex);
		entity.setClause(clauseValue);
	
		columnIndex = cursor.getColumnIndex(mPrescriptionColumnName);
		long prescriptionValue = cursor.getLong(columnIndex);
		entity.setPrescription(prescriptionValue);
	
		return entity;
	}
}
