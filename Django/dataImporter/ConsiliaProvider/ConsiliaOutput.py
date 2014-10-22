# -*- coding: utf-8 -*-
import sys
import os
import codecs
import re
from dataImporter.Utils.Utility import *

class PrescriptionWriter:
    def __init__(self):
        self.__file_name__ = os.path.dirname(__file__) + "\\debug.txt"
        
    def create(self):
        try:
            os.remove(self.__file_name__)
        except Exception,ex:
            print ex
    
    def __write_single_prescription__(self, prescription):
        if prescription:
            self.__file_writer__.write( "name:" + prescription['name']+ " quantity:" + str(prescription['quantity']) + " unit:" + prescription['unit'] + "\n")
            for component in prescription['components']:
                self.__file_writer__.write(Utility.convert_dict_to_string(component) + "\n")
            self.__file_writer__.write( "comment:" + prescription['comment'] + "\n")
    
    def write_single_prescription(self, prescription):
        self.__file_writer__ = codecs.open(self.__file_name__, 'a+', 'utf-8', 'ignore')
        self.__write_single_prescription__(prescription)
        self.__file_writer__.close()
        
    def write_prescriptions(self, prescriptions, writer):
        self.__file_writer__ = writer
        #self.__file_writer__ = codecs.open(self.__file_name__, 'a+', 'utf-8', 'ignore')
        map(self.__write_single_prescription__, prescriptions)
        #self.__file_writer__.close()

class ConsiliaWriter:
    def __init__(self):
        self.__file_name__ = os.path.dirname(__file__) + "\\debug.txt"
        self.__write_single_detail__ = self.__write_single_detail_full__
        self.__prescription_writer__ = PrescriptionWriter()
        
    def __write_if_contains_number__(self, text):
        items = text.split("\n")
        print text
        for item in items:
            m = re.compile(ur'\d克').search(item)
            if m:
                self.__file_writer__.write(item + "\n")
            
    def __write_single_detail_contains_number__(self, detail):
        for key, value in detail.items():
            if not type(value) is str:
                continue
            self.__write_if_contains_number__(value)
            

    def __write_single_detail_full__(self, detail):
#         self.__file_writer__.write("index:" + str(detail[u'order']) + "\n")
#         self.__file_writer__.write("description:" + detail[u'description'] + "\n")
#         self.__file_writer__.write("comment:" + detail[u'comment'] + "\n")
        
        self.__file_writer__.write(str(detail[u'order']) + "\n")
        self.__file_writer__.write(detail[u'description'] + "\n")
        
        self.__prescription_writer__.write_prescriptions(detail['prescriptions'], self.__file_writer__)
        
        self.__file_writer__.write(detail[u'comment'] + "\n")
        
    def __write_single_consilia__(self, consilia):
        map(self.__write_single_detail__, consilia['details'])
        
    def write_consilias(self, consilias):
        self.__file_writer__ = codecs.open(self.__file_name__, 'w', 'utf-8', 'ignore')
        map(self.__write_single_consilia__, consilias)
        self.__file_writer__.close()
        
    def write_contains_number(self, consilias):
        self.__write_single_detail__ = self.__write_single_detail_contains_number__
        self.write_consilias(consilias)
    
if __name__ == "__main__":
    print "no data"
