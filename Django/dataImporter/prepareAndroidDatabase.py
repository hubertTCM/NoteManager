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
        
        
class ColumnSchema:
    def __init__(self, name, columnIndex, dbType, isPrimaryKey):
        self.name = name
        self.dbType = dbType
        self.isPrimaryKey = isPrimaryKey
        self.index = columnIndex
        
        
    
    def getName(self):
        return self.name
    
    def getIndex(self):
        return self.index
    
    def getDbType(self):
        return self.dbType
    
    def getIsPrimary(self):
        return self.isPrimaryKey
        
class TableSchema:
    def __init__(self, name):
        self.columns = []
        self.name = name
    
    def addColumn(self, column):
        self.columns.append(column)
        
    def getColumns(self):
        return self.columns
    
    def getName(self):
        return self.name
    
    def getPrimaryColumn(self):
        for column in self.columns:
            if column.getIsPrimary():
                return column
        return None

class DatabaseSchema:
    def __init__(self):
        self.__tables__ = []
    
    def addTable(self, table):
        self.__tables__.append(table)
    
    def getTables(self):
        return self.__tables__

class SchemaCreator:
    def __init__(self, db_file):
        self.db_file = db_file
                
    def createSchema(self):
        schema = DatabaseSchema()
        cx = sqlite3.connect(self.db_file)
        cu=cx.cursor()
        cu.execute("SELECT tbl_name, sql FROM sqlite_master WHERE type = 'table'")
        items = cu.fetchall()
        
        for tbl_name, sql in items:
            columns = cu.execute('PRAGMA table_info(' + tbl_name + ')')
            schema.addTable(self.__createTableSchema__(tbl_name, columns))
        
        return schema
    
    def __createTableSchema__(self, tbl_name, columns):
        table = TableSchema(tbl_name)
        index = 0
        for cid, name, columnType, notnull, dflt_value, pk in columns:
            column = ColumnSchema(name, index, columnType, pk)
            table.addColumn(column)
            ++index;
        return table

# TBD

class Helper:
    def __init__(self):
        words = []
        words.append("clause")
        words.append("person")
        words.append("herb")
        words.append("alias")
        words.append("unit")
        words.append("disease")
        words.append("component")
        words.append("medical")
        words.append("note")
        words.append("prescription")
        words.append("method")
        words.append("data")
        words.append("source")
        words.append("connection")
        words.append("detail")
        words.append("treatment")
        
        self.wordsMap = {}
        for word in words:
            self.wordsMap[word] = self.convertFirstCharToUpper(word)
        self.wordsMap["yian"] = "YiAn"
        self.wordsMap["_id"] = ""
        
        typeMap = {}
        typeMap["integer"] = "long"
        typeMap["varchar"] = "String"
        typeMap["text"] = "String"
        typeMap["real"] = "double"
        
        self.typeMap = typeMap
    
    def convertFirstCharToUpper(self, name):
        return name[:1].upper() + name[1:]
    
    def convertFirstCharToLower(self, name):
        return name[:1].lower() + name[1:]
    
    def getJavaTypeName(self, dbType):
        temp = dbType.lower()
        for key in self.typeMap:
            if temp.startswith(key):
                return self.typeMap[key]
        return temp
    
    def getFormalizedName(self, name):
        if name == "_id":
            return "Id"
        
        prefix = "TCM_"
        formalizedName = name
        if name.startswith(prefix):
            formalizedName = name[len(prefix):]
        
        for key in self.wordsMap:
            value = self.wordsMap[key]
            formalizedName = formalizedName.replace(key, value)

        return self.convertFirstCharToUpper(formalizedName)

class EntityCodeGenerator:
    def __init__(self, tableSchema):
        self.schema = tableSchema
        self.helper = Helper()
        
    def getTable(self):
        return self.schema
        
    def getClassName(self):
        tableName = self.schema.getName()
        formalizedName = self.helper.getFormalizedName(tableName)
        return formalizedName + "Entity"
    
    def __getMemberName__(self, column):
        return "m" + self.helper.getFormalizedName(column.getName())
    
    def __addMembers__(self, codes):
        temp = []
        for column in self.schema.getColumns():
            memberName = self.__getMemberName__(column)
            javaType = self.helper.getJavaTypeName(column.getDbType())
            temp.append("private " + javaType + " "+ memberName + ";")
        
        for item in temp:
            codes.append("\t" + item)
        
        return codes

    def __addFunctions__(self, codes):
        temp = []
        for column in self.schema.getColumns():
            # get..
            propertyName = self.getGetPropertyName(column)
            javaType = self.helper.getJavaTypeName(column.getDbType())
            temp.append("public " + javaType + " "+ propertyName + "() {")
            temp.append("\treturn " + self.__getMemberName__(column) + ";")
            temp.append("}")
            
            temp.append("")
            
            if not column.getIsPrimary():
                #set..
                propertyName = self.getSetPropertyName(column)
                temp.append("public void "+ propertyName + "(" + javaType + " value) {")
                temp.append("\t" + self.__getMemberName__(column) + " = " + "value;")
                temp.append("}")
                temp.append("")
        
        for item in temp:
            codes.append("\t" + item)
        
        return codes
    
    def __addConstructor__(self, codes):
        temp=[]
        
        primaryColumn = self.schema.getPrimaryColumn()
        if primaryColumn:
            javaType = self.helper.getJavaTypeName(primaryColumn.getDbType())
            parameterName = self.helper.getFormalizedName(primaryColumn.getName())
            parameterName = parameterName[:1].lower() + parameterName[1:]
            
            temp.append("public " + self.getClassName() + "( " + javaType + " " + parameterName + " )" +  " {")
            temp.append("\t" + self.__getMemberName__(primaryColumn) + " = " + parameterName + ";")
            temp.append("}")
        
        for item in temp:
            codes.append("\t" + item)
        
        return codes
        
    
    def getGetPropertyName(self, column):
        return "get" + self.helper.getFormalizedName(column.getName())
    
    def getSetPropertyName(self, column):
        return "set" + self.helper.getFormalizedName(column.getName())
    
    def generate(self):
        codes = []
        codes.append("public class " + self.getClassName() + " {")
        
        self.__addMembers__(codes)
        
        codes.append("")
        
        self.__addConstructor__(codes)
        
        codes.append("")
        
        self.__addFunctions__(codes)
        
        codes.append("}")
        
        return codes

class DaoCodeGenerator:
    def __init__(self, entityGeneraror):
        self.schema = entityGeneraror.getTable()
        self.entityGenerator = entityGeneraror
        self.helper = Helper()
    
    def __getColumnNameProperty__(self, column):
        return "m" + self.helper.getFormalizedName(column.getName()) + "ColumnName"
    
    def __addDataMember__(self, codes):
        temp = []
        
        for column in self.schema.getColumns():
            memberName = self.__getColumnNameProperty__(column)
            temp.append("private String " + memberName + " = \"" + column.getName() + "\";")
        
        temp.append("")
        temp.append("private SQLiteDatabase mDatabase;")
        
        codes.extend(["\t" + item for item in temp])
        return codes
    
    def __createContructor__(self, codes):
        temp = []
        
        temp.append("public " + self.getClassName()+ "(SQLiteDatabase database) {")
        temp.append("\tmDatabase = database;")
        temp.append("}")
        
        codes.extend(["\t" + item for item in temp])
        return codes
    
    def __createLoadAll__(self, codes):
        temp = []
        entityClassName = self.entityGenerator.getClassName()
        entityClassNameTemplate = "<" + entityClassName + ">"
        
        temp.append("public List" + entityClassNameTemplate + " loadAll() {")
        temp.append("\tCursor cursor = mDatabase.rawQuery(\"select * from " + self.schema.getName() +"\", null);")
        temp.append("\treturn loadAll(cursor);")
        temp.append("}")
        
        temp.append("private List" + entityClassNameTemplate + " loadAll(Cursor cursor) {")
        temp.append("\tVector" + entityClassNameTemplate + " items = new Vector" + entityClassNameTemplate + "();")
        temp.append("\tfor (cursor.moveToFirst(); !cursor.isAfterLast(); cursor.moveToNext()) {")
        temp.append("\t\titems.add(" + self.__getCreateEntityFunctionName__() + "(cursor));")
        temp.append("\t}")
        temp.append("\treturn items;")
        temp.append("}")
        
        codes.extend(["\t" + item for item in temp])
        return codes
        
    def __createLoad__(self, codes):
        column = self.schema.getPrimaryColumn()
        if not column:
            return column
            
        temp = []
        
        formalizedColumnName = self.helper.getFormalizedName(column.getName())
        formalizedColumnName = self.helper.convertFirstCharToLower(formalizedColumnName)
        javaType = self.helper.getJavaTypeName(column.getDbType())
        
        temp.append("public " + self.entityGenerator.getClassName() + " load("  + javaType + " " + formalizedColumnName+ ") {")
        sql = "\"select * from " + self.schema.getName() + " where " + column.getName() +" = ?\""
        
        whereArgs = "new String[]{" + " new StringBuilder().append(" + formalizedColumnName +  ").toString() }"
        temp.append("\tString[] whereArgs = " + whereArgs + ";")
        temp.append("\tCursor cursor = mDatabase.rawQuery(" + sql + ", whereArgs);")
        temp.append("\treturn " + self.__getCreateEntityFunctionName__() + "(cursor);")
        temp.append("}")
        
        codes.extend(["\t" + item for item in temp])
        return codes
        
    def __addPublicFunctions__(self, codes):
        self.__createContructor__(codes)
        codes.append("")
        self.__createLoadAll__(codes)
        codes.append("")
        self.__createLoad__(codes)
        return codes
    
    def __getCreateEntityFunctionName__(self):
        return "createEntity";
    
    def __addConvertFunction__(self, codes):
        temp = []
        
        entityClass = self.entityGenerator.getClassName()
        temp.append("private " + entityClass + " "+ self.__getCreateEntityFunctionName__() + "(Cursor cursor) {")
        temp.append("\tint columnIndex = 0;")
        
        entityObject = "entity"
        column = self.schema.getPrimaryColumn()
        
        def create():
            temp.append("")
            columnValueProperty = self.helper.getFormalizedName(column.getName())
            columnValueProperty = self.helper.convertFirstCharToLower(columnValueProperty) + "Value"
            columnNameProperty = self.__getColumnNameProperty__(column)
            javaType = self.helper.getJavaTypeName(column.getDbType())
            getFunctionName = "get" + self.helper.convertFirstCharToUpper(javaType)
            temp.append("\tcolumnIndex = cursor.getColumnIndex("+ columnNameProperty +");")
            temp.append("\t" + javaType + " " + columnValueProperty + " = cursor." +getFunctionName + "(columnIndex);" )
            return columnValueProperty
        
        if column:
            columnValueProperty = create()
            temp.append("\t" + entityClass + " " + entityObject + " = new " + entityClass + "(" + columnValueProperty + ");")
        else:
            temp.append("\t" + entityClass + " " + entityObject + " = new " + entityClass + "();")
        
        
        for column in self.schema.getColumns():
            if not column.getIsPrimary():
                columnValueProperty = create()
                temp.append("\t" + entityObject + "." + self.entityGenerator.getSetPropertyName(column) + "(" + columnValueProperty + ");")

        temp.append("")
        temp.append("\treturn " + entityObject + ";")
        temp.append("}")
        
        codes.extend(["\t" + item for item in temp])
        return codes;
    
    def getClassName(self):
        tableName = self.schema.getName()
        return self.helper.getFormalizedName(tableName) + "Dao"
    
    def generate(self):
        codes = []
        
        codes.append("import java.util.List;")
        codes.append("import java.util.Vector;")
        codes.append("import java.lang.StringBuilder;")
        codes.append("")
        codes.append("import android.database.Cursor;")
        codes.append("import android.database.sqlite.SQLiteDatabase;")
        codes.append("")
        
        codes.append("public class " + self.getClassName() + " {")
        codes.append("")
        
        self.__addDataMember__(codes)
        codes.append("")
        
        self.__addPublicFunctions__(codes)
        codes.append("")
        
        self.__addConvertFunction__(codes)
        codes.append("}")
        return codes

class CodeGenerator:
    def __init__(self, db_file, package_name, to_folder):
        creator = SchemaCreator(db_file)
        self.schema = creator.createSchema()
        self.to_folder = to_folder
        self.package = package_name

    def __generateTableCode__(self, table):
        generators = []
        entitityGenerator = EntityCodeGenerator(table)
        generators.append(entitityGenerator)
        generators.append(DaoCodeGenerator(entitityGenerator))
        
        for generator in generators:
            className = generator.getClassName()
            codeFile = open(to_folder + '\\' + className+ ".java",'w')
            codeFile.write("package " + self.package + ";\n")
            codeFile.write("\n")
            
            for code in generator.generate():
                codeFile.write(code + "\n")
            codeFile.close()

    def generateCode(self):   
        for table in self.schema.getTables():
            self.__generateTableCode__(table)

if __name__ == "__main__":
#     android_db = create_android_database_file()
#     update_to_android_schema(android_db)
    
    android_db = r'D:\Personal\NoteManager\Django\TCM\noteManager_android.db'
    to_folder = r"D:\Personal\NoteManager\Android\generateCode\\"
    g = CodeGenerator(android_db, "com.hubert.notesmanager.dal.orm", to_folder)
    g.generateCode()
    print "done"
    
