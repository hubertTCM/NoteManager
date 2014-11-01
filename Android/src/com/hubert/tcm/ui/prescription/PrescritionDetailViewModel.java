package com.hubert.tcm.ui.prescription;

import java.util.List;
import java.util.Vector;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.widget.*;

import com.hubert.tcm.R;
import com.hubert.tcm.dal.DatabaseHelper;
import com.hubert.tcm.dal.orm.*;

public class PrescritionDetailViewModel {

    private Context mContext;
    private PrescriptionEntity mEntity;
    private SQLiteOpenHelper mDbHelper;
    
    
    public PrescritionDetailViewModel(long id, Context context ){
        mContext = context;
        mDbHelper = new DatabaseHelper(context);        

        SQLiteDatabase db = mDbHelper.getReadableDatabase();
        PrescriptionDao dao = new PrescriptionDao(db);
        mEntity = dao.load(id);
    }
    
    public String getName(){
        return mEntity.getName();
    }
    
    public PrescriptionComponentAdapter getComponentAdapter(){
        return new PrescriptionComponentAdapter(mContext, R.layout.prescription_component, getCompositions());
    }
    
    public ArrayAdapter<String> getCluaseAdapter(){
        SQLiteDatabase db = mDbHelper.getReadableDatabase();
        PrescriptionClauseConnectionDao dao = new PrescriptionClauseConnectionDao(db);
        ClauseDao clauseDao = new ClauseDao(db);
        Vector<String> items = new Vector<String>();
        for(PrescriptionClauseConnectionEntity connectionEntity : dao.loadByPrescription(mEntity.getId())){
            items.add(clauseDao.load(connectionEntity.getClauseId()).getContent());
        }
        return new ArrayAdapter<String>(mContext, android.R.layout.simple_list_item_1, items);
    }
    
    private List<PrescriptionComponentEntity> getCompositions(){
        SQLiteDatabase db = mDbHelper.getReadableDatabase();
        PrescriptionComponentDao dao = new PrescriptionComponentDao(db);
        return dao.loadByPrescription(mEntity.getId());
    }
}
