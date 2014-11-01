package com.hubert.tcm.dal;

import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import com.hubert.tcm.R;

import android.content.Context;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SQLiteOpenHelper;

public class DatabaseHelper extends SQLiteOpenHelper {

    // The Android's default system path of your application database.
    private static String DB_PATH = null;// "/data/data/YOUR_PACKAGE/databases/";

    private static String mDbName = "note_manager_android.db";

    // private SQLiteDatabase myDataBase;

    private final Context mContext;

    /**
     * Constructor Takes and keeps a reference of the passed context in order to
     * access to the application assets and resources.
     * 
     * @param context
     */
    public DatabaseHelper(Context context) {
        super(context, mDbName, null, 1);
        this.mContext = context;
        String packageName = context.getPackageName();
        DB_PATH = String.format("//data//data//%s//databases//", packageName);

        try {
            createDatabase();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }
    
    private void createDatabase() throws IOException {
        File db = new File(DB_PATH, mDbName);
        if (!db.exists()) {
            new File(DB_PATH).mkdirs();
            db.createNewFile();
            copyFromZipFile();
        }
    }

    private void copyFromZipFile() throws IOException {
        InputStream inputStream = mContext.getResources().openRawResource( R.raw.note_manager_android );
        OutputStream outputStream = new FileOutputStream(new File(DB_PATH, mDbName).getAbsolutePath());
        try {
            byte[] buffer = new byte[1024];
            int count;
            while ((count = inputStream.read(buffer)) > 0){
                outputStream.write(buffer, 0, count);
            }
        } finally {
            outputStream.flush();
            outputStream.close();
            inputStream.close();
        }
    }

    @Override
    public void onCreate(SQLiteDatabase db) {

    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {

    }
}
