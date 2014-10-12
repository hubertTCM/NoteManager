package com.hubert.notesmanager.ui.main;

import java.util.List;
import java.util.Vector;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import com.hubert.notesmanager.dal.DatabaseHelper;
import com.hubert.notesmanager.dal.orm.*;

public class ClauseViewModel {
	private ClauseEntity mEntity;
	private SQLiteOpenHelper mDbHelper;
	
	public ClauseViewModel(SQLiteOpenHelper dbHelper, ClauseEntity entity){
		mEntity = entity;
		mDbHelper = dbHelper;
	}
	
	public String getContent(){
		return mEntity.getContent();
	}
	
	public List<PrescriptionEntity> getRelatedPrescriptions(){
		SQLiteDatabase db = mDbHelper.getReadableDatabase();
		List<PrescriptionEntity> prescriptions = new Vector<PrescriptionEntity>();
		PrescriptionClauseConnectionDao connectionDao = new PrescriptionClauseConnectionDao(db);
		PrescriptionDao prescriptionDao = new PrescriptionDao(db);
		for(PrescriptionClauseConnectionEntity connectionEntity : connectionDao.loadByClause(mEntity.getId())){
			prescriptions.add(prescriptionDao.load(connectionEntity.getPrescriptionId()));
		}
		return prescriptions;
	}

}
