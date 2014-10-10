package com.hubert.notesmanager.dal.imp;
import java.util.List;
import java.util.Vector;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;

import com.hubert.notesmanager.dal.IDataProvider;
import com.hubert.notesmanager.dal.orm.ClauseDao;
import com.hubert.notesmanager.dal.orm.ClauseEntity;
import com.hubert.notesmanager.data.CategoryItem;

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
	public List<ClauseEntity> getTiaoWens() {
		SQLiteDatabase database = mDbHelper.getReadableDatabase();
		ClauseDao dao = new ClauseDao(database);
		
		return dao.loadAll();
	}

}
