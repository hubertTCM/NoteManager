package com.hubert.notesmanager.ui;

import java.util.List;

import com.hubert.notesmanager.dal.imp.DataProvider;
import com.hubert.notesmanager.dal.orm.ClauseEntity;
import com.hubert.notesmanager.data.CategoryItem;

import android.R;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.TextView;

public class TiaoWenAdapter extends ArrayAdapter<ClauseEntity>{
	private LayoutInflater mInflater;
	
	public TiaoWenAdapter(Context context){
		super(context, R.layout.simple_list_item_1);

		DataProvider provider = new DataProvider(context);
		super.addAll(provider.getTiaoWens());
		
		mInflater = LayoutInflater.from(context);
	}

	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		ClauseEntity item = getItem(position);
		TextView textView = null;
//		ImageView itemIcon = null;
		if(convertView == null){
			convertView = mInflater.inflate(R.layout.simple_list_item_1, null);
		}
		textView = (TextView) convertView.findViewById(R.id.text1); 
		textView.setText(item.getContent());
//		itemIcon = (ImageView) convertView.findViewById(R.id.item_icon);
//		itemTitle.setText(item.getTitle());
//		itemIcon.setBackground(item.getIcon());
		return convertView;
	}

}
