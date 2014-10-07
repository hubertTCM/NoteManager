package com.hubert.notesmanager.dal.imp;
import java.util.List;
import java.util.Vector;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

import com.hubert.notesmanager.dal.IDataProvider;
import com.hubert.notesmanager.data.CategoryItem;
import com.hubert.notesmanager.data.TiaoWen;

public class DataProvider implements IDataProvider{
	private DatabaseHelper mDbHelper;
	
	public DataProvider(Context context){
		mDbHelper = new DatabaseHelper(context, "note_manager_android.db");
	}

	@Override
	public List<CategoryItem> getCategories() {
		Vector<CategoryItem> categories = new Vector<CategoryItem>();
		categories.add(new CategoryItem("经方", 1));
		return categories;
	}

	@Override
	public List<TiaoWen> getTiaoWen() {
		SQLiteDatabase database = mDbHelper.getReadableDatabase();
		Cursor cursor = database.rawQuery("select * from TCM_clause", null);
		
		Vector<TiaoWen> items = new Vector<TiaoWen>();
		for (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {
		    // do what you need with the cursor here
			TiaoWen item = new TiaoWen(cursor.getInt(0), cursor.getString(3));
			items.add(item);
		}
		
		//SQLiteQueryBuilder
		//SQLiteQueryBuilder 
		//db.op
		// TODO Auto-generated method stub
		return items;
	}

}
