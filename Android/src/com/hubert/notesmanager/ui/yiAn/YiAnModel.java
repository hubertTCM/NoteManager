package com.hubert.notesmanager.ui.yiAn;

import java.util.*;

import android.content.*;
import android.view.LayoutInflater;

import com.hubert.notesmanager.dal.DatabaseHelper;
import com.hubert.notesmanager.dal.orm.*;

public class YiAnModel {
    private long mYiAnId;
    private Context mContext;
    private DatabaseHelper mDbHelper;
    private List<YiAnDetailModel> mDetails;
    
    public YiAnModel(long yiAnId, Context context){
        mYiAnId = yiAnId;
        mContext = context;
        mDbHelper = new DatabaseHelper(mContext);
    }
    
    public YiAnDetailEntity getYiAnDetail(long order){
        return null;
    }
    
    public List<YiAnDetailModel> getDetails(){
        if (mDetails != null){
            return mDetails;
        }
        mDetails = new Vector<YiAnDetailModel>();
        YiAnDetailDao dao = new YiAnDetailDao(mDbHelper.getReadableDatabase());
        for (YiAnDetailEntity detail : dao.loadByYiAn(mYiAnId)){
            mDetails.add(new YiAnDetailModel(detail, mDbHelper));
        }
        
        return mDetails;
    }
    

}
