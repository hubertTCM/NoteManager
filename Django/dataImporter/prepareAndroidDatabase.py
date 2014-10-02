import os
import shutil
import sqlite3
from shutil import copyfile

#django_database = r''

def create_android_database_file():
    source_database = r'D:\Personal\NoteManager\Django\TCM\noteManager.db'
    to_database = r'D:\Personal\NoteManager\Django\TCM\noteManager_android.db'
    
    copyfile(source_database, to_database)
    return to_database

def update_to_android_schema(db_file):
    cx = sqlite3.connect(db_file)
    cu=cx.cursor()
    cu.execute("SELECT tbl_name, sql FROM sqlite_master WHERE type = 'table'")
    items = cu.fetchall()
    
    contains_android_metadata = False
    cu.execute('PRAGMA writable_schema = on')
    for tbl_name, sql in items:
        if tbl_name == "android_metadata":
            contains_android_metadata = True
            
        print "name:", tbl_name, "\n sql:", sql
        changed_sql = sql.replace("id", "_id")
        changed_sql = changed_sql.replace("__id", "_id")
        if (changed_sql != sql):
            new_sql = "update sqlite_master set sql ='" + changed_sql + "' where tbl_name = '"  + tbl_name + "'  and type = 'table'"
            print new_sql
            cu.execute("update sqlite_master set sql ='" + changed_sql + "' where tbl_name = '"  + tbl_name + "'  and type = 'table'")
    
    cu.execute('PRAGMA writable_schema = off')
    
    if not contains_android_metadata:
        cu.execute('CREATE TABLE "android_metadata" ("locale" TEXT DEFAULT \'en_US\')')
        cu.execute('INSERT INTO "android_metadata" VALUES (\'en_US\')')
        cx.commit()

if __name__ == "__main__":
    android_db = create_android_database_file()
    update_to_android_schema(android_db)
    print "done"
    
