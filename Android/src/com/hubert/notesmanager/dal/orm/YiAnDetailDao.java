package com.hubert.notesmanager.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class YiAnDetailDao {

    private String mIdColumnName = "_id";
    private String mOrderColumnName = "order";
    private String mYiAnIdColumnName = "yiAnId";
    private String mDescriptionColumnName = "description";
    private String mCommentsColumnName = "comment";
    private String mComeFromIdColumnName = "comeFrom_id";
    
    private SQLiteDatabase mDatabase;

    public YiAnDetailDao(SQLiteDatabase database) {
        mDatabase = database;
    }

    public List<YiAnDetailEntity> loadAll() {
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yiandetail", null);
        List<YiAnDetailEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }

    public List<YiAnDetailEntity> loadFirst() {
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yiandetail where [order] = \"1\"", null);
        List<YiAnDetailEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }
    
    public List<YiAnDetailEntity> loadByYiAn(long yiAnId){
        String[] whereArgs = new String[]{ Long.toString(yiAnId) };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yiandetail where yiAnId = ?", whereArgs);
        List<YiAnDetailEntity> items = loadAll(cursor);
        cursor.close();
        return items;
        
    }

    public YiAnDetailEntity load(long id) {
        String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_yiandetail where _id = ?", whereArgs);
        cursor.moveToFirst();
        YiAnDetailEntity item= createEntity(cursor);
        cursor.close();
        return item;
    }

    private YiAnDetailEntity createEntity(Cursor cursor) {
        int columnIndex = 0;
    
        columnIndex = cursor.getColumnIndex(mIdColumnName);
        long idValue = cursor.getLong(columnIndex);
        YiAnDetailEntity entity = new YiAnDetailEntity(idValue);
    
        columnIndex = cursor.getColumnIndex(mOrderColumnName);
        long orderValue = cursor.getLong(columnIndex);
        entity.setOrder(orderValue);
    
        columnIndex = cursor.getColumnIndex(mYiAnIdColumnName);
        long yiAnIdValue = cursor.getLong(columnIndex);
        entity.setYiAnId(yiAnIdValue);
    
        columnIndex = cursor.getColumnIndex(mDescriptionColumnName);
        String descriptionValue = cursor.getString(columnIndex);
        entity.setDescription(descriptionValue);
    
        columnIndex = cursor.getColumnIndex(mCommentsColumnName);
        String commentsValue = cursor.getString(columnIndex);
        entity.setComments(commentsValue);
    
        columnIndex = cursor.getColumnIndex(mComeFromIdColumnName);
        long comeFromIdValue = cursor.getLong(columnIndex);
        entity.setComeFromId(comeFromIdValue);
    
        return entity;
    }
    
    private List<YiAnDetailEntity> loadAll(Cursor cursor) {
        Vector<YiAnDetailEntity> items = new Vector<YiAnDetailEntity>();
        for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
            items.add(createEntity(cursor));
        }
        return items;
    }
}
