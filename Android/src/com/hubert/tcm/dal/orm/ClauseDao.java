package com.hubert.tcm.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class ClauseDao {

    private String mIdColumnName = "_id";
    private String mComeFromIdColumnName = "comeFrom_id";
    private String mIndexColumnName = "index";
    private String mContentColumnName = "content";
    
    private SQLiteDatabase mDatabase;

    public ClauseDao(SQLiteDatabase database) {
        mDatabase = database;
    }

    public List<ClauseEntity> loadAll() {
        Cursor cursor = mDatabase.rawQuery("select * from TCM_clause", null);
        List<ClauseEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }

    public ClauseEntity load(long id) {
        String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_clause where _id = ?", whereArgs);
        cursor.moveToFirst();
        ClauseEntity item= createEntity(cursor);
        cursor.close();
        return item;
    }

    private ClauseEntity createEntity(Cursor cursor) {
        int columnIndex = 0;
    
        columnIndex = cursor.getColumnIndex(mIdColumnName);
        long idValue = cursor.getLong(columnIndex);
        ClauseEntity entity = new ClauseEntity(idValue);
    
        columnIndex = cursor.getColumnIndex(mComeFromIdColumnName);
        long comeFromIdValue = cursor.getLong(columnIndex);
        entity.setComeFromId(comeFromIdValue);
    
        columnIndex = cursor.getColumnIndex(mIndexColumnName);
        long indexValue = cursor.getLong(columnIndex);
        entity.setIndex(indexValue);
    
        columnIndex = cursor.getColumnIndex(mContentColumnName);
        String contentValue = cursor.getString(columnIndex);
        entity.setContent(contentValue);
    
        return entity;
    }
    
    private List<ClauseEntity> loadAll(Cursor cursor) {
        Vector<ClauseEntity> items = new Vector<ClauseEntity>();
        for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
            items.add(createEntity(cursor));
        }
        return items;
    }
}
