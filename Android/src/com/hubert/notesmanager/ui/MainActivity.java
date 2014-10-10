package com.hubert.notesmanager.ui;

import java.lang.reflect.Field;

import com.hubert.notesmanager.R;
import com.hubert.notesmanager.data.CategoryItem;

import android.support.v4.widget.DrawerLayout;
import android.app.Activity;
import android.app.ActionBar;
import android.app.Fragment;
import android.app.FragmentTransaction;
import android.content.Context;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewConfiguration;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.SpinnerAdapter;
import android.widget.TextView;
import android.os.Build;

public class MainActivity extends Activity implements INavigationCategoryCallback{
	private DrawerLayout mDrawerLayout;
	private ContentFragment mContentFragment;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
		mDrawerLayout = (DrawerLayout) findViewById(R.id.drawer_layout);
		//drawerLayout.setDrawerShadow(R.drawable.ic_launcher, GravityCompat.START);
		//mCategoryFragment = (CategoryFragment) getFragmentManager()
		//		.findFragmentById(R.id.left_drawer);

		ActionBar actionBar = getActionBar();
		actionBar.setDisplayHomeAsUpEnabled(true);
		actionBar.setHomeButtonEnabled(true);
		actionBar.setDisplayShowHomeEnabled(false);

		// mTitle = getTitle();

		// ListView lv = (ListView) this.findViewById(R.id.left_drawer);
		// String[] values = new String[] { "Android", "iPhone",
		// "WindowsMobile",
		// "Blackberry", "WebOS", "Ubuntu", "Windows7", "Max OS X",
		// "Linux", "OS/2" };
		//
		// ArrayAdapter<String> files = new ArrayAdapter<String>(this,
		// android.R.layout.simple_list_item_1, values);
		//
		// lv.setAdapter(files);

		// getActionBar().setDisplayHomeAsUpEnabled(true);
		// getActionBar().setHomeButtonEnabled(true);

		// SpinnerAdapter
		// ActionBar actionBar = getActionBar();
		// actionBar.setNavigationMode(ActionBar.NAVIGATION_MODE_LIST);
		// actionBar.setListNavigationCallbacks(new CategoryAdapter(this, 0),
		// new CategoryNavigationListener(getApplicationContext()));

		//
		// try {
		// ViewConfiguration mconfig = ViewConfiguration.get(this);
		// Field menuKeyField =
		// ViewConfiguration.class.getDeclaredField("sHasPermanentMenuKey");
		// if(menuKeyField != null) {
		// menuKeyField.setAccessible(true);
		// menuKeyField.setBoolean(mconfig, false);
		// }
		// } catch (Exception ex) {
		// }

		if (savedInstanceState == null) {
			FragmentTransaction ft = getFragmentManager().beginTransaction();
			mContentFragment = new ContentFragment();
			ft.add(R.id.container, mContentFragment);
			ft.commit();
		}
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}

	@Override
	public void onSelect(CategoryItem item) {
		getActionBar().setTitle(item.getName());
		mContentFragment.onSelect(item);
	}
}
