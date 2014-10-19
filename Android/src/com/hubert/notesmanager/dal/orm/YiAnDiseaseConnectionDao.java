package com.hubert.notesmanager.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class YiAnDiseaseConnectionDao {

    private String mIdColumnName = "_id";
    private String mYiAnIdColumnName = "yiAn_id";
    private String mDiseaseIdColumnName = "disease_id";
    
    private SQLiteDatabase mDatabase;

    public YiAnDiseaseConnectionDao(SQLiteDatabase database) {
        mDatabase = database;
    }

    public List<YiAnDiseaseConnectionEntity> loadAll() {
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yiandiseaseconnection", null);
        List<YiAnDiseaseConnectionEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }
    
    public List<YiAnDiseaseConnectionEntity> loadByYiAnId(long id){
        String[] whereArgs = new String[]{Long.toString(id)};
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yiandiseaseconnection where yiAn_id=?", whereArgs);
        List<YiAnDiseaseConnectionEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }

    public YiAnDiseaseConnectionEntity load(long id) {
        String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yiandiseaseconnection where _id = ?", whereArgs);
        cursor.moveToFirst();
        YiAnDiseaseConnectionEntity item= createEntity(cursor);
        cursor.close();
        return item;
    }

    private YiAnDiseaseConnectionEntity createEntity(Cursor cursor) {
        int columnIndex = 0;
    
        columnIndex = cursor.getColumnIndex(mIdColumnName);
        long idValue = cursor.getLong(columnIndex);
        YiAnDiseaseConnectionEntity entity = new YiAnDiseaseConnectionEntity(idValue);
    
        columnIndex = cursor.getColumnIndex(mYiAnIdColumnName);
        long yiAnIdValue = cursor.getLong(columnIndex);
        entity.setYiAnId(yiAnIdValue);
    
        columnIndex = cursor.getColumnIndex(mDiseaseIdColumnName);
        String diseaseIdValue = cursor.getString(columnIndex);
        entity.setDiseaseId(diseaseIdValue);
    
        return entity;
    }
    
    private List<YiAnDiseaseConnectionEntity> loadAll(Cursor cursor) {
        Vector<YiAnDiseaseConnectionEntity> items = new Vector<YiAnDiseaseConnectionEntity>();
        for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
            items.add(createEntity(cursor));
        }
        return items;
    }
}
