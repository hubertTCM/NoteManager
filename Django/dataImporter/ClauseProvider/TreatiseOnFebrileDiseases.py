# -*- coding: utf-8 -*-

import codecs

import os
import re
import sys

from PrescriptionParser import *

reload(sys)
sys.setdefaultencoding("utf-8")

def append_ancestors_to_system_path(levels):
    parent = os.path.dirname(__file__)
    for i in range(levels):
        sys.path.append(parent)
        parent = os.path.abspath(os.path.join(parent, ".."))
        
append_ancestors_to_system_path(3)

from dataImporter.Utils.Utility import *
#sys.setdefaultencoding('utf-8')


class FebribleDiseaseProvider:
    def __init__(self):
        self.__sourceFile__ = os.path.dirname(__file__) + '\\shl.txt'    
    
    def __createClause__(self, index, item_contents):
        items = [item.strip() for item in item_contents if len(item.strip()) > 0]
        comeFrom = {u'bookTitle': u'伤寒论'} 
        content = ''
        if len(items) > 0:
            content = '\n'.join(items)
            parser = PrescriptionParser(content, u'方', QuantityAdjustor()) 
            content, prescriptions = parser.extractPrescriptions() 
            for prescription in prescriptions:
                prescription.update({'comeFrom' : comeFrom})           
            
        return {'index':index, 'content':content, 'prescriptions':prescriptions, 'comeFrom' : comeFrom}
    
    def getAllClauses(self):
        clauses = []
        
        shl = codecs.open(self.__sourceFile__, 'r', 'utf-8')
        item_contents = []
        
        index = 0
        for line in shl:            
            matches = re.findall(ur"\s*[\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u96f6]{1,3}\u3001", line)
            if len(matches) > 0 and line.strip().index(u'\u3001') < 4:
                if (len(item_contents) > 0):
                    clauses.append(self.__createClause__(index, item_contents))
                index += 1
                item_contents = []
                
                item_contents.append(line.strip())
            else:    
                item_contents.append(line.strip())
                
        shl.close() 
        
        clauses.append(self.__createClause__(index, item_contents))
        return clauses


if __name__ == "__main__":     
    debugFile = os.path.dirname(__file__) + '\\debug.txt'
    debugWriter = codecs.open(debugFile, 'w', 'utf-8', 'ignore')
    
    provider = FebribleDiseaseProvider()
    clauses = provider.getAllClauses()    
    for item in clauses:
        debugWriter.write(item['content'] + "\n")
        print_prescription_list(item['prescriptions'])
        print "=="
          
    debugWriter.close()
    print "done"