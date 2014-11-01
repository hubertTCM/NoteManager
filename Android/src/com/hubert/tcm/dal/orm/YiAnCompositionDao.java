package com.hubert.tcm.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class YiAnCompositionDao {

    private String mIdColumnName = "_id";
    private String mPrescriptionIdColumnName = "prescription_id";
    private String mComponentColumnName = "component";
    private String mUnitIdColumnName = "unit_id";
    private String mQuantityColumnName = "quantity";
    private String mCommentColumnName = "comment";
    
    private SQLiteDatabase mDatabase;

    public YiAnCompositionDao(SQLiteDatabase database) {
        mDatabase = database;
    }

    public List<YiAnCompositionEntity> loadAll() {
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yiancomposition", null);
        List<YiAnCompositionEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }
    

    public List<YiAnCompositionEntity> loadByPrescriptionId(long prescriptionId) {
        String[] whereArgs = new String[]{Long.toString(prescriptionId)};
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yiancomposition where prescription_id = ?", whereArgs);
        List<YiAnCompositionEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }

    public YiAnCompositionEntity load(long id) {
        String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yiancomposition where _id = ?", whereArgs);
        cursor.moveToFirst();
        YiAnCompositionEntity item= createEntity(cursor);
        cursor.close();
        return item;
    }

    private YiAnCompositionEntity createEntity(Cursor cursor) {
        int columnIndex = 0;
    
        columnIndex = cursor.getColumnIndex(mIdColumnName);
        long idValue = cursor.getLong(columnIndex);
        YiAnCompositionEntity entity = new YiAnCompositionEntity(idValue);
    
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
    
    private List<YiAnCompositionEntity> loadAll(Cursor cursor) {
        Vector<YiAnCompositionEntity> items = new Vector<YiAnCompositionEntity>();
        for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
            items.add(createEntity(cursor));
        }
        return items;
    }
}
