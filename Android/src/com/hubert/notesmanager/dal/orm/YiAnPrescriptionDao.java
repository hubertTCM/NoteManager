package com.hubert.notesmanager.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class YiAnPrescriptionDao {

    private String mIdColumnName = "_id";
    private String mYiAnDetailIdColumnName = "yiAnDetail_id";
    private String mNameColumnName = "name";
    private String mAllHerbTextColumnName = "allHerbText";
    private String mUnitColumnName = "unit";
    private String mQuantityColumnName = "quantity";
    private String mCommentColumnName = "comment";
    
    private SQLiteDatabase mDatabase;

    public YiAnPrescriptionDao(SQLiteDatabase database) {
        mDatabase = database;
    }

    public List<YiAnPrescriptionEntity> loadAll() {
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yianprescription", null);
        List<YiAnPrescriptionEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }
    
    public List<YiAnPrescriptionEntity> loadByYiAnDetailId(long yiAnDetailId) {
        String[] whereArgs = new String[]{Long.toString(yiAnDetailId)};
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yianprescription where yiAnDetail_id = ?", whereArgs);
        List<YiAnPrescriptionEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }

    public YiAnPrescriptionEntity load(long id) {
        String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yianprescription where _id = ?", whereArgs);
        cursor.moveToFirst();
        YiAnPrescriptionEntity item= createEntity(cursor);
        cursor.close();
        return item;
    }

    private YiAnPrescriptionEntity createEntity(Cursor cursor) {
        int columnIndex = 0;
    
        columnIndex = cursor.getColumnIndex(mIdColumnName);
        long idValue = cursor.getLong(columnIndex);
        YiAnPrescriptionEntity entity = new YiAnPrescriptionEntity(idValue);
    
        columnIndex = cursor.getColumnIndex(mYiAnDetailIdColumnName);
        long yiAnDetailIdValue = cursor.getLong(columnIndex);
        entity.setYiAnDetailId(yiAnDetailIdValue);
    
        columnIndex = cursor.getColumnIndex(mNameColumnName);
        String nameValue = cursor.getString(columnIndex);
        entity.setName(nameValue);
    
        columnIndex = cursor.getColumnIndex(mAllHerbTextColumnName);
        String allHerbTextValue = cursor.getString(columnIndex);
        entity.setAllHerbText(allHerbTextValue);
    
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
    
    private List<YiAnPrescriptionEntity> loadAll(Cursor cursor) {
        Vector<YiAnPrescriptionEntity> items = new Vector<YiAnPrescriptionEntity>();
        for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
            items.add(createEntity(cursor));
        }
        return items;
    }
}
