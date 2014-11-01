package com.hubert.tcm.ui.main;

import java.util.List;
import java.util.Vector;

import com.hubert.tcm.data.CategoryItem;

import android.R;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.SpinnerAdapter;
import android.widget.TextView;

public class CategoryAdapter extends BaseAdapter{
	private LayoutInflater mInflater;
	private List<CategoryItem> items;
	
	public CategoryAdapter(Context context) {
		items = new Vector<CategoryItem>();
		items.add(new CategoryItem("�?方", 1));
		
		mInflater = LayoutInflater.from(context);
	}

	@Override
	public int getCount() {
		return items.size();
	}

	@Override
	public CategoryItem getItem(int paramInt) {
		return items.get(paramInt);
	}

	@Override
	public long getItemId(int paramInt) {
		// TODO Auto-generated method stub
		return paramInt;
	}



	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		CategoryItem item = getItem(position);
		TextView textView = null;
//		ImageView itemIcon = null;
		if(convertView == null){
			convertView = mInflater.inflate(R.layout.simple_list_item_1, null);
		}
		textView = (TextView) convertView.findViewById(R.id.text1); 
		textView.setText(item.getName());
//		itemIcon = (ImageView) convertView.findViewById(R.id.item_icon);
//		itemTitle.setText(item.getTitle());
//		itemIcon.setBackground(item.getIcon());
		return convertView;
	}

}
