package com.hubert.tcm.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class PrescriptionComponentDao {

    private String mIdColumnName = "_id";
    private String mPrescriptionIdColumnName = "prescription_id";
    private String mComponentColumnName = "component";
    private String mUnitIdColumnName = "unit_id";
    private String mQuantityColumnName = "quantity";
    private String mCommentColumnName = "comment";
    
    private SQLiteDatabase mDatabase;

    public PrescriptionComponentDao(SQLiteDatabase database) {
        mDatabase = database;
    }

    public List<PrescriptionComponentEntity> loadAll() {
        Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptioncomponent", null);
        List<PrescriptionComponentEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }
    
    public List<PrescriptionComponentEntity> loadByPrescription(long prescriptionId) {
        String[] whereArgs = new String[]{Long.toString(prescriptionId)};
        String sql = "select * from TCM_prescriptioncomponent where prescription_id = ?";
        Cursor cursor = mDatabase.rawQuery(sql, whereArgs);
        List<PrescriptionComponentEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }

    public PrescriptionComponentEntity load(long id) {
        String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_prescriptioncomponent where _id = ?", whereArgs);
        cursor.moveToFirst();
        PrescriptionComponentEntity item= createEntity(cursor);
        cursor.close();
        return item;
    }
    

    private PrescriptionComponentEntity createEntity(Cursor cursor) {
        int columnIndex = 0;
    
        columnIndex = cursor.getColumnIndex(mIdColumnName);
        long idValue = cursor.getLong(columnIndex);
        PrescriptionComponentEntity entity = new PrescriptionComponentEntity(idValue);
    
        columnIndex = cursor.getColumnIndex(mPrescriptionIdColumnName);
        long prescriptionIdValue = cursor.getLong(columnIndex);
        entity.setPrescriptionId(prescriptionIdValue);
    
        columnIndex = cursor.getColumnIndex(mComponentColumnName);
        String componentValue = cursor.getString(columnIndex);
        entity.setComponent(componentValue);
    
        columnIndex = cursor.getColumnIndex(mUnitIdColumnName);
        String unitIdValue = cursor.getString(columnIndex);
        entity.setUnitId(unitIdValue);
    
        columnIndex = cursor.getColumnIndex(mQuantityColumnName);
        double quantityValue = cursor.getDouble(columnIndex);
        entity.setQuantity(quantityValue);
    
        columnIndex = cursor.getColumnIndex(mCommentColumnName);
        String commentValue = cursor.getString(columnIndex);
        entity.setComment(commentValue);
    
        return entity;
    }
    
    private List<PrescriptionComponentEntity> loadAll(Cursor cursor) {
        Vector<PrescriptionComponentEntity> items = new Vector<PrescriptionComponentEntity>();
        for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
            items.add(createEntity(cursor));
        }
        return items;
    }
}
