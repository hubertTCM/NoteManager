package com.hubert.tcm.yian.ui;

import java.util.*;

import com.hubert.tcm.R;
import com.hubert.tcm.dal.DatabaseHelper;
import com.hubert.tcm.dal.orm.*;
import android.app.Activity;
import android.content.*;
import android.os.Bundle;
import android.view.*;
import android.view.View.OnClickListener;
import android.widget.*;

public class YiAnSummaryActivity extends Activity {
    private Vector<YiAnSummaryModel> mAllSummary;
    private ListView mListViewSummary;
    private ArrayAdapter<YiAnSummaryModel> mSummaryAdapter;

    private boolean mBeShuffle = false;

    public YiAnSummaryActivity() {
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_yian_summary);

        setUp();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu items for use in the action bar
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.activity_yian_summary, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
        case R.id.action_shfulle:
            mBeShuffle = !mBeShuffle;
            if (mBeShuffle) {
                Collections.shuffle(mAllSummary);
            } else {
                Collections.sort(mAllSummary, new DefaultComparator());
            }

            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    mSummaryAdapter.notifyDataSetChanged();
                }
            });
            return true;
        }
        return super.onOptionsItemSelected(item);
    }

    private void setUp() {
        mListViewSummary = (ListView) findViewById(R.id.listview_yian);
        DatabaseHelper dbHelper = new DatabaseHelper(this);
        YiAnDetailDao dao = new YiAnDetailDao(dbHelper.getReadableDatabase());
        mAllSummary = new Vector<YiAnSummaryModel>();
        for (YiAnDetailEntity entity : dao.loadFirst()) {
            mAllSummary.add(new YiAnSummaryModel(dbHelper, entity));
        }
        mSummaryAdapter = createSummaryAdapter();
        mListViewSummary.setAdapter(mSummaryAdapter);
    }

    private ArrayAdapter<YiAnSummaryModel> createSummaryAdapter() {
        ArrayAdapter<YiAnSummaryModel> adapter = new ArrayAdapter<YiAnSummaryModel>(
                this, android.R.layout.simple_list_item_2, mAllSummary) {
            @Override
            public View getView(int position, View convertView, ViewGroup parent) {
                TwoLineListItem item;
                if (convertView == null) {
                    LayoutInflater inflater = LayoutInflater
                            .from(YiAnSummaryActivity.this);
                    item = (TwoLineListItem) inflater.inflate(
                            android.R.layout.simple_list_item_2, null);
                    item.getText2().setOnClickListener(new OnClickListener() {
                        @Override
                        public void onClick(View paramView) {
                            YiAnSummaryModel summaryModel = (YiAnSummaryModel) paramView
                                    .getTag();
                            YiAnDetailEntity entity = summaryModel.getEntity();
                            Intent intent = new Intent(
                                    YiAnSummaryActivity.this,
                                    YiAnDetailActivity.class);
                            intent.putExtra(YiAnDetailActivity.YIAN_ID,
                                    entity.getYiAnId());
                            intent.putExtra(YiAnDetailActivity.YIAN_NAME,
                                    summaryModel.getName());
                            YiAnSummaryActivity.this.startActivity(intent);
                        }
                    });
                } else {
                    item = (TwoLineListItem) convertView;
                }
                YiAnSummaryModel data = getItem(position);
                item.getText1().setText(data.getName());
                item.getText2().setText(data.getSummary());
                item.getText2().setTag(data);
                return item;
            }
        };
        return adapter;
    }

//    private class RandomComparator implements Comparator<YiAnSummaryModel> {
//        private Random mRandom = new Random();
//
//        @Override
//        public int compare(YiAnSummaryModel x, YiAnSummaryModel y) {
//            long randomX = mRandom.nextInt();
//            long randomY = mRandom.nextInt();
//            if (Math.abs(randomX) < Math.abs(randomY)) {
//                return -1;
//            }
//            return 1;
//        }
//    }

    private class DefaultComparator implements Comparator<YiAnSummaryModel> {
        @Override
        public int compare(YiAnSummaryModel x, YiAnSummaryModel y) {
            if (x.getEntity().getId() < y.getEntity().getId()) {
                return -1;
            }
            return 1;
        }
    }
}
