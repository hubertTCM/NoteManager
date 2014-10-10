package com.hubert.notesmanager.data;


public class CategoryItem {
	private String mName;
	private long mId;
	public CategoryItem(String name, long id){
		mName = name;
		mId = id;
		
		
	}
	
	
	public String getName(){
		return mName;
	}
	
	public long getId(){
		return mId;
	}
}
