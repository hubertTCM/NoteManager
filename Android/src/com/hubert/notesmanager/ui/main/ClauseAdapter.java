package com.hubert.notesmanager.ui.main;

import java.util.List;

import com.hubert.notesmanager.R;
import com.hubert.notesmanager.dal.DatabaseHelper;
import com.hubert.notesmanager.dal.orm.ClauseDao;
import com.hubert.notesmanager.dal.orm.ClauseEntity;
import com.hubert.notesmanager.dal.orm.PrescriptionEntity;
import com.hubert.notesmanager.data.CategoryItem;
import com.hubert.notesmanager.ui.prescription.PrescriptionActivity;

import android.content.Context;
import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

public class ClauseAdapter extends ArrayAdapter<ClauseViewModel>{
	private LayoutInflater mInflater;
	private Context mContext;
	
	public ClauseAdapter(Context context){
		super(context, R.layout.cluase_detail);

		DatabaseHelper helper = new DatabaseHelper(context);
		ClauseDao dao = new ClauseDao(helper.getReadableDatabase());
		for(ClauseEntity item : dao.loadAll()){
			super.add(new ClauseViewModel(helper, item));
		}
		
		mInflater = LayoutInflater.from(context);
		mContext = context;
	}

	@Override
	public View getView(int position, View convertView, ViewGroup parent) {
		ClauseViewModel item = getItem(position);
		TextView textView = null;
		if(convertView == null){
			convertView = mInflater.inflate(R.layout.cluase_detail, null);
		}
		textView = (TextView) convertView.findViewById(R.id.textview_clause_content); 
		textView.setText(item.getContent());
		LinearLayout l = (LinearLayout)convertView.findViewById(R.id.prescrptions);
		l.removeAllViews();
		
		for (PrescriptionEntity entity : item.getRelatedPrescriptions()){
		    l.addView(createButton(entity));
		}
		
		return convertView;
	}
	
	private Button createButton(PrescriptionEntity entity){
	    Button b = new Button(mContext);
	    b.setText(entity.getName());
	    b.setTag(entity);
	    
	    b.setOnClickListener(new OnClickListener(){
	        @Override
	        public void onClick(View paramView){
	            PrescriptionEntity prescription = (PrescriptionEntity)paramView.getTag();
//	            Toast toast = Toast.makeText(mContext, prescription.getName(), 1);
//	            toast.show();
	            
	            Intent intent = new Intent(mContext, PrescriptionActivity.class);
	            intent.putExtra(PrescriptionActivity.PRESCRIPTION_ID, prescription.getId());
	            mContext.startActivity(intent);
	        }
	    });
	    
	    return b;
	}

}
