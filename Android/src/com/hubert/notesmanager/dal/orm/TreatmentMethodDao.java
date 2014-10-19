package com.hubert.notesmanager.dal.orm;

import java.util.List;
import java.util.Vector;
import java.lang.StringBuilder;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

public class TreatmentMethodDao {

    private String mNameColumnName = "name";
    
    private SQLiteDatabase mDatabase;

    public TreatmentMethodDao(SQLiteDatabase database) {
        mDatabase = database;
    }

    public List<TreatmentMethodEntity> loadAll() {
        Cursor cursor = mDatabase.rawQuery("select * from TCM_treatmentmethod", null);
        List<TreatmentMethodEntity> items = loadAll(cursor);
        cursor.close();
        return items;
    }

    public TreatmentMethodEntity load(String name) {
        String[] whereArgs = new String[]{ new StringBuilder().append(name).toString() };
        Cursor cursor = mDatabase.rawQuery("select * from TCM_treatmentmethod where name = ?", whereArgs);
        cursor.moveToFirst();
        TreatmentMethodEntity item= createEntity(cursor);
        cursor.close();
        return item;
    }

    private TreatmentMethodEntity createEntity(Cursor cursor) {
        int columnIndex = 0;
    
        columnIndex = cursor.getColumnIndex(mNameColumnName);
        String nameValue = cursor.getString(columnIndex);
        TreatmentMethodEntity entity = new TreatmentMethodEntity(nameValue);
    
        return entity;
    }
    
    private List<TreatmentMethodEntity> loadAll(Cursor cursor) {
        Vector<TreatmentMethodEntity> items = new Vector<TreatmentMethodEntity>();
        for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
            items.add(createEntity(cursor));
        }
        return items;
    }
}
