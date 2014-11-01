package com.hubert.tcm.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class PrescriptionDao {

    private String mIdColumnName = "_id";
    private String mNameColumnName = "name";
    private String mAllHerbTextColumnName = "allHerbText";
    private String mComeFromIdColumnName = "comeFrom_id";
    private String mCommentColumnName = "comment";
    
    private SQLiteDatabase mDatabase;

    public PrescriptionDao(SQLiteDatabase database) {
        mDatabase = database;
    }

    public List<PrescriptionEntity> loadAll() {
        Cursor cursor = mDatabase.rawQuery("select * from TCM_prescription", null);
        List<PrescriptionEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }

    public PrescriptionEntity load(long id) {
        String[] whereArgs = new String[]{ new StringBuilder().append(id).toString() };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_prescription where _id = ?", whereArgs);
        cursor.moveToFirst();
        PrescriptionEntity item= createEntity(cursor);
        cursor.close();
        return item;
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
    
        columnIndex = cursor.getColumnIndex(mComeFromIdColumnName);
        long comeFromIdValue = cursor.getLong(columnIndex);
        entity.setComeFromId(comeFromIdValue);
    
        columnIndex = cursor.getColumnIndex(mCommentColumnName);
        String commentValue = cursor.getString(columnIndex);
        entity.setComment(commentValue);
    
        return entity;
    }
    
    private List<PrescriptionEntity> loadAll(Cursor cursor) {
        Vector<PrescriptionEntity> items = new Vector<PrescriptionEntity>();
        for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
            items.add(createEntity(cursor));
        }
        return items;
    }
}
