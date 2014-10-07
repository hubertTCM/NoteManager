package com.hubert.notesmanager.dal.imp;

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import android.content.Context;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SQLiteOpenHelper;

public class DatabaseHelper extends SQLiteOpenHelper{

	//The Android's default system path of your application database.
    private static String DB_PATH = null;//"/data/data/YOUR_PACKAGE/databases/";
 
    private String mDbName;
 
    //private SQLiteDatabase myDataBase; 
 
    private final Context mContext;
 
    /**
     * Constructor
     * Takes and keeps a reference of the passed context in order to access to the application assets and resources.
     * @param context
     */
    public DatabaseHelper(Context context, String dbName) {
    	super(context, dbName, null, 1);
        this.mContext = context;
        String packageName = context.getPackageName();
        DB_PATH = String.format("//data//data//%s//databases//", packageName);
        mDbName = dbName;
        
        try {
			createDatabase();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
    }	
    
 
  /**
     * Creates a empty database on the system and rewrites it with your own database.
     * */
    private void createDatabase() throws IOException{ 
    	boolean dbExist = checkDatabase(); 
    	if(dbExist){
    		//do nothing - database already exist
    	}else{ 
    		//By calling this method and empty database will be created into the default system path
            //of your application so we are gonna be able to overwrite that database with our database.
        	this.getReadableDatabase(); 
        	try { 
    			copyDatabase(); 
    		} catch (IOException e) { 
        		throw new Error("Error copying database"); 
        	}
    	} 
    }
 
    /**
     * Check if the database already exist to avoid re-copying the file each time you open the application.
     * @return true if it exists, false if it doesn't
     */
    private boolean checkDatabase(){ 
    	SQLiteDatabase checkDB = null; 
    	try{
    		String myPath = DB_PATH + mDbName;
    		checkDB = SQLiteDatabase.openDatabase(myPath, null, SQLiteDatabase.OPEN_READONLY); 
    	}catch(SQLiteException e){ 
    		//database does't exist yet. 
    	}
 
    	if(checkDB != null){ 
    		checkDB.close(); 
    	}
 
    	return checkDB != null ? true : false;
    }
 
    /**
     * Copies your database from your local assets-folder to the just created empty database in the
     * system folder, from where it can be accessed and handled.
     * This is done by transfering bytestream.
     * */
    private void copyDatabase() throws IOException{
    	
    	String[] allFiles = mContext.getAssets().list("/");
    	
 
    	//Open your local db as the input stream
    	InputStream myInput = mContext.getAssets().open(mDbName); 
    	// Path to the just created empty db
    	String outFileName = DB_PATH + mDbName; 
    	//Open the empty db as the output stream
    	OutputStream myOutput = new FileOutputStream(outFileName); 
    	//transfer bytes from the inputfile to the outputfile
    	byte[] buffer = new byte[1024];
    	int length;
    	while ((length = myInput.read(buffer))>0){
    		myOutput.write(buffer, 0, length);
    	}
 
    	//Close the streams
    	myOutput.flush();
    	myOutput.close();
    	myInput.close();
    }
  
	@Override
	public void onCreate(SQLiteDatabase db) {
 
	}
 
	@Override
	public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
 
	}
 }
