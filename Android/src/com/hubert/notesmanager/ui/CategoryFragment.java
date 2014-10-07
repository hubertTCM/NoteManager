package com.hubert.notesmanager.ui;

import com.hubert.notesmanager.R;

import android.app.Activity;
import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListAdapter;
import android.widget.ListView;

public class CategoryFragment extends Fragment {
	private ListView mLvCategory;
	private CategoryAdapter mAdapterCategory;
	private INavigationCategoryCallback mCallback;
	
	public void Init(){
		
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		mLvCategory = (ListView) inflater.inflate(R.layout.listview_category, container, false);

		/*String[] values = new String[] { "Android", "iPhone", "WindowsMobile",
				"Blackberry", "WebOS", "Ubuntu", "Windows7", "Max OS X",
				"Linux", "OS/2" };

		ArrayAdapter<String> files = new ArrayAdapter<String>(getActivity(),
				android.R.layout.simple_list_item_1, values);*/

		mAdapterCategory = new CategoryAdapter(this.getActivity()); 
		mLvCategory.setAdapter(mAdapterCategory);
		
		mLvCategory.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
                SelectItem(position);
            }
        });
		
		return mLvCategory;
	}

    @Override
    public void onAttach(Activity activity) {
        super.onAttach(activity);
        try {
            mCallback = (INavigationCategoryCallback) activity;
        } catch (ClassCastException e) {
            throw new ClassCastException("Activity must implement NavigationDrawerCallbacks.");
        }
    }

    @Override
    public void onDetach() {
        super.onDetach();
        mCallback = null;
    }
	
    private void SelectItem(int position){
    	if (mCallback != null){
    		mCallback.onSelect(mAdapterCategory.getItem(position));
    	}
    }
   
}
