package com.hubert.notesmanager.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class PrescriptionClauseConnectionDao {

    private String mIdColumnName = "_id";
    private String mClauseIdColumnName = "clause_id";
    private String mPrescriptionIdColumnName = "prescription_id";
    
    private SQLiteDatabase mDatabase;

    public PrescriptionClauseConnectionDao(SQLiteDatabase database) {
        mDatabase = database;
    }

    public List<PrescriptionClauseConnectionEntity> loadAll() {
        Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptionclauseconnection", null);
        List<PrescriptionClauseConnectionEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }

    public PrescriptionClauseConnectionEntity load(long id) {
        String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptionclauseconnection where _id = ?", whereArgs);
        cursor.moveToFirst();
        PrescriptionClauseConnectionEntity item= createEntity(cursor);
        cursor.close();
        return item;
    }
	
	public List<PrescriptionClauseConnectionEntity> loadByClause(long id){
        return load("clause_id", id);
	}
	
    public List<PrescriptionClauseConnectionEntity> loadByPrescription(long id){
        return load("prescription_id", id);
    }

    private List<PrescriptionClauseConnectionEntity> load(String columnName, long id){
        String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptionclauseconnection where " + columnName + " = ?", whereArgs);
        List<PrescriptionClauseConnectionEntity> items= loadAll(cursor);
        cursor.close();
        return items;
    }
    private PrescriptionClauseConnectionEntity createEntity(Cursor cursor) {
        int columnIndex = 0;
    
        columnIndex = cursor.getColumnIndex(mIdColumnName);
        long idValue = cursor.getLong(columnIndex);
        PrescriptionClauseConnectionEntity entity = new PrescriptionClauseConnectionEntity(idValue);
    
        columnIndex = cursor.getColumnIndex(mClauseIdColumnName);
        long clauseIdValue = cursor.getLong(columnIndex);
        entity.setClauseId(clauseIdValue);
    
        columnIndex = cursor.getColumnIndex(mPrescriptionIdColumnName);
        long prescriptionIdValue = cursor.getLong(columnIndex);
        entity.setPrescriptionId(prescriptionIdValue);
    
        return entity;
    }
    
    private List<PrescriptionClauseConnectionEntity> loadAll(Cursor cursor) {
        Vector<PrescriptionClauseConnectionEntity> items = new Vector<PrescriptionClauseConnectionEntity>();
        for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
            items.add(createEntity(cursor));
        }
        return items;
    }
}
