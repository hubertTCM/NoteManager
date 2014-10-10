package com.hubert.notesmanager.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class PrescriptionDao {

	private String mIdColumnName = "_id";
	private String mNameColumnName = "name";
	private String mAllHerbTextColumnName = "allHerbText";
	private String mComeFromColumnName = "comeFrom_id";
	private String mCommentColumnName = "comment";
	
	private SQLiteDatabase mDatabase;

	public PrescriptionDao(SQLiteDatabase database) {
		mDatabase = database;
	}

	public List<PrescriptionEntity> loadAll() {
		Cursor cursor = mDatabase.rawQuery("select * from TCM_prescription", null);
		return loadAll(cursor);
	}
	private List<PrescriptionEntity> loadAll(Cursor cursor) {
		Vector<PrescriptionEntity> items = new Vector<PrescriptionEntity>();
		for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
			items.add(createEntity(cursor));
		}
		return items;
	}

	public PrescriptionEntity load(long id) {
		String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
		Cursor cursor = mDatabase.rawQuery("select * from TCM_prescription where _id = ?", whereArgs);
		return createEntity(cursor);
	}

	private PrescriptionEntity createEntity(Cursor cursor) {
		int columnIndex = 0;
	
		columnIndex = cursor.getColumnIndex(mIdColumnName);
		long idValue = cursor.getLong(columnIndex);
		PrescriptionEntity entity = new PrescriptionEntity(idValue);
	
		columnIndex = cursor.getColumnIndex(mNameColumnName);
		String nameValue = cursor.getString(columnIndex);
		entity.setName(nameValue);
	
		columnIndex = cursor.getColumnIndex(mAllHerbTextColumnName);
		String allHerbTextValue = cursor.getString(columnIndex);
		entity.setAllHerbText(allHerbTextValue);
	
		columnIndex = cursor.getColumnIndex(mComeFromColumnName);
		long comeFromValue = cursor.getLong(columnIndex);
		entity.setComeFrom(comeFromValue);
	
		columnIndex = cursor.getColumnIndex(mCommentColumnName);
		String commentValue = cursor.getString(columnIndex);
		entity.setComment(commentValue);
	
		return entity;
	}
}
