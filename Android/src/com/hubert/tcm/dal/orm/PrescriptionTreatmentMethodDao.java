package com.hubert.tcm.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class PrescriptionTreatmentMethodDao {

    private String mIdColumnName = "_id";
    private String mMethodIdColumnName = "method_id";
    private String mPrescriptionIdColumnName = "prescription_id";
    
    private SQLiteDatabase mDatabase;

    public PrescriptionTreatmentMethodDao(SQLiteDatabase database) {
        mDatabase = database;
    }

    public List<PrescriptionTreatmentMethodEntity> loadAll() {
        Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptiontreatmentmethod", null);
        List<PrescriptionTreatmentMethodEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }

    public PrescriptionTreatmentMethodEntity load(long id) {
        String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptiontreatmentmethod where _id = ?", whereArgs);
        cursor.moveToFirst();
        PrescriptionTreatmentMethodEntity item= createEntity(cursor);
        cursor.close();
        return item;
    }

    private PrescriptionTreatmentMethodEntity createEntity(Cursor cursor) {
        int columnIndex = 0;
    
        columnIndex = cursor.getColumnIndex(mIdColumnName);
        long idValue = cursor.getLong(columnIndex);
        PrescriptionTreatmentMethodEntity entity = new PrescriptionTreatmentMethodEntity(idValue);
    
        columnIndex = cursor.getColumnIndex(mMethodIdColumnName);
        String methodIdValue = cursor.getString(columnIndex);
        entity.setMethodId(methodIdValue);
    
        columnIndex = cursor.getColumnIndex(mPrescriptionIdColumnName);
        long prescriptionIdValue = cursor.getLong(columnIndex);
        entity.setPrescriptionId(prescriptionIdValue);
    
        return entity;
    }
    
    private List<PrescriptionTreatmentMethodEntity> loadAll(Cursor cursor) {
        Vector<PrescriptionTreatmentMethodEntity> items = new Vector<PrescriptionTreatmentMethodEntity>();
        for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
            items.add(createEntity(cursor));
        }
        return items;
    }
}
