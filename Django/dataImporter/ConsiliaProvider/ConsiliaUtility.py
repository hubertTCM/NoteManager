from dataImporter.prescriptionImporter import herbUtility
# -*- coding: utf-8 -*-
import sys
import os
import codecs
import re
from dataImporter.Utils.Utility import *
from dataImporter.Utils.HerbUtil import *

class Logger:
    def __init__(self):
        self.__file_name__ = os.path.dirname(__file__) + "\\debug.txt"
        
    def empty_log(self):
        try:
            os.remove(self.__file_name__)
        except Exception,ex:
            print ex
            
    def write_line(self, line):
        self.__file_writer__ = codecs.open(self.__file_name__, 'a+', 'utf-8', 'ignore')
        self.__file_writer__.write(line + "\n")
        self.__file_writer__.close()
        self.__file_writer__ = None
    
    def write_lines(self, lines):
        self.__file_writer__ = codecs.open(self.__file_name__, 'a+', 'utf-8', 'ignore')
        for line in lines:
            self.__file_writer__.write(line + "\n")
        self.__file_writer__.close()
        self.__file_writer__ = None
        
        

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
        
    def __write_line__(self, line):
        if line and len(line) > 0:
            self.__file_writer__.write(line + "\n")
        
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
        self.__write_line__(detail[u'description'])
        
        self.__prescription_writer__.write_prescriptions(detail['prescriptions'], self.__file_writer__)
        
        self.__write_line__(detail[u'comment'])
        
    def __write_single_consilia__(self, consilia):
        self.__file_writer__.write(" ".join(consilia['diseaseNames']) + "\n")
        map(self.__write_single_detail__, consilia['details'])
        self.__file_writer__.write("\n")
        
    def write_consilias(self, consilias):
        self.__file_writer__ = codecs.open(self.__file_name__, 'w', 'utf-8', 'ignore')
        map(self.__write_single_consilia__, consilias)
        self.__file_writer__.close()
        
    def write_contains_number(self, consilias):
        self.__write_single_detail__ = self.__write_single_detail_contains_number__
        self.write_consilias(consilias)
    
class ConsiliaHelper:
    def get_un_imported_herbs(self, consilias):
        herbs = []
        for item in consilias:
            for detail in item['details']:
                for prescription in detail['prescriptions']:
                    for component in prescription['components']:
                        herb = component['medical']
                        if not herbUtility.isHerb(herb) and not herb in herbs:
                            herbs.append(herb)
                            if len(herb) == 1:
                                herbs.append(prescription['_debug'])
        return herbs
                        
    
if __name__ == "__main__":
    print "no data"
