# -*- coding: utf-8 -*-
import sys
import os
import codecs
import re

class ConsiliaWriter:
    def __init__(self):
        self.__file_name__ = os.path.dirname(__file__) + "\\consiliaInfo.txt"
        self.__write_single_detail__ = self.__write_single_detail_full__
        
    def __write_if_contains_nuber__(self, text):
        m = re.compile(ur'\d克').search(text)
        if m:
            self.__file_writer__.write(text + "\n")
            
    def __write_single_detail_contains_number__(self, detail):
        comment = detail['comment']
        self.__write_if_contains_nuber__(comment)
            
            
    def __write_description_contains_number__(self, detail):
        descriptions = detail['description'].split("\n")
        map(self.__write_if_contains_nuber__, descriptions)
        #self.__write_if_contains_nuber__(description)
        
    def __write_single_detail_full__(self, detail):
        self.__file_writer__.write("index:" + str(detail[u'order']) + "\n")
        self.__file_writer__.write("description:" + detail[u'description'] + "\n")
        self.__file_writer__.write("comment:" + detail[u'comment'] + "\n")
        
    def __write_single_consilia__(self, consilia):
        map(self.__write_single_detail__, consilia['details'])
        
    def write_consilias(self, consilias):
        self.__file_writer__ = codecs.open(self.__file_name__, 'w', 'utf-8', 'ignore')
        map(self.__write_single_consilia__, consilias)
        self.__file_writer__.close()
        
    def write_comment_contains_number(self, consilias):
        self.__write_single_detail__ = self.__write_single_detail_contains_number__
        self.write_consilias(consilias)
        
        
    def write_description_contains_number(self, consilias):
        self.__write_single_detail__ = self.__write_description_contains_number__
        self.write_consilias(consilias)
        
if __name__ == "__main__":
    print "no data"
