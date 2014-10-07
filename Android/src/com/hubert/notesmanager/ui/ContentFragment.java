package com.hubert.notesmanager.ui;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;

import com.hubert.notesmanager.R;
import com.hubert.notesmanager.dal.imp.DataProvider;
import com.hubert.notesmanager.data.CategoryItem;


/**
 * A placeholder fragment containing a simple view.
 */
public class ContentFragment extends Fragment implements INavigationCategoryCallback{
	
	//private TextView mTextView;
	private ListView mLvItems;

	public ContentFragment() {
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.content_main, container,
				false);
		//mTextView = (TextView)rootView.findViewById(R.id.test);
		mLvItems = (ListView)rootView.findViewById(R.id.list_content);

		// ListView list = (ListView)
		// rootView.findViewById(R.id.summaryList);

		/*
		 * String[] values = new String[] { "Android", "iPhone",
		 * "WindowsMobile", "Blackberry", "WebOS", "Ubuntu", "Windows7",
		 * "Max OS X", "Linux", "OS/2" };
		 * 
		 * ArrayAdapter<String> files = new
		 * ArrayAdapter<String>(getActivity(),
		 * android.R.layout.simple_list_item_1, values);
		 * 
		 * list.setAdapter(files);
		 */

		return rootView;
	}

	@Override
	public void onSelect(CategoryItem item) {
		// TODO Auto-generated method stub
		//this.mTextView.setText(item.getName());
		if (mLvItems == null){
			return;
		}
		
		ListAdapter adapter = null;
		if(item.getId() == 1){
			adapter = new TiaoWenAdapter(getActivity());
		}
		mLvItems.setAdapter(adapter);
	}
}
