package com.hubert.notesmanager.data;

public class TiaoWen {
	private int mId;
	private String mContent;
	public TiaoWen(int id, String content){
		mId = id;
		mContent = content;
	}
	
	public int getId(){
		return mId;
	}
	
	public String getContent(){
		return mContent;
	}
}
