# -*- coding: utf-8 -*-
import os
import re
import sys


def append_ancestors_to_system_path(levels):
    parent = os.path.dirname(__file__)
    for i in range(levels):
        sys.path.append(parent)
        parent = os.path.abspath(os.path.join(parent, ".."))
        
append_ancestors_to_system_path(3)

from dataImporter.Utils.Utility import *
from ComponentAdjustor import *

#制附片60克(久煎) 
#葱白60克 
class SingleComponentParser1:
    def __init__(self, text):
        self._source_text = text
        self._herb = text
        self._quantity_unit = None
        self._apply_quantity_to_others = False
        self._comments = None 
        
    def __parse_quantity_comment__(self, text):
        quantity_unit_pattern = ur"([\d]+[^（(]+)"
        comment_pattern = ur"[（(]([\W]+)[)）]"
        successed = False
        # quantity（comment）
        m = re.compile(quantity_unit_pattern + comment_pattern).match(text)
        if m:
            self._quantity_unit = m.group(1).strip()
            self._comments = m.group(2).strip()
            successed = True
            
        if not successed:#（comment）quantity
            m = re.compile(comment_pattern + ur"([各]*)" + quantity_unit_pattern).match(text)
            if m:
                self._quantity_unit = m.group(3).strip()
                self._comments = m.group(1).strip()
                if len(m.group(2)) > 0:
                    self._apply_quantity_to_others = True
                    
                successed = True
                
        if not successed:#quantity
            m = re.compile(quantity_unit_pattern).match(text)
            if m:
                successed = True
                self._quantity_unit = m.group(1).strip()
                successed = True
                
        if not successed:#comment
            m = re.compile(comment_pattern).match(text)
            if m:
                self._comments = m.group(1).strip()
    
    def __parse_normal_medical_name__(self):
        pattern = ur"([^（）\d各]+)(\d*\W*)"
        m = re.compile(pattern).match(self._source_text)
        if m:
            self._herb = m.group(1).strip()
            self.__parse_quantity_comment__(m.group(2).strip())

    def get_component(self):   
        m = MedicalNameParser(self._source_text)
        herb, other = m.split_with_medical_name()
        if herb:
            self._herb = herb
            self.__parse_quantity_comment__(other)
        else:
            self.__parse_normal_medical_name__()
        
        quantity, unit = (None, None)
        if self._quantity_unit:
            quantity_parser = QuantityParser1(self._quantity_unit)
            quantity, unit = quantity_parser.parse()
         
        component = {'medical': self._herb, 'quantity': quantity, 'unit': unit, 'comments': self._comments, 
                     "applyQuantityToOthers":self._apply_quantity_to_others} 
        
        
        #print Utility.convert_dict_to_string(component)
        return component


class SingleComponentParser2:
    def __init__(self, text, component_adjustor):
        self._source_text = text
        self._herb = text
        self._quantity_unit = None
        self._apply_quantity_to_others = False
        self._comments = None 
        self._component_adjustor = component_adjustor
        
    def __parse_quantity_comment__(self, text):
        quantity_unit_pattern = ur"([一二三四五六七八九十半百]+[^（(]+)"
        comment_pattern = ur"[（(]([\W]+)[)）]"
        successed = False
        # quantity（comment）
        m = re.compile(quantity_unit_pattern + comment_pattern).match(text)
        if m:
            self._quantity_unit = m.group(1).strip()
            self._comments = m.group(2).strip()
            successed = True
            
        if not successed:#（comment）quantity
            m = re.compile(comment_pattern + ur"([各]*)" + quantity_unit_pattern).match(text)
            if m:
                self._quantity_unit = m.group(3).strip()
                self._comments = m.group(1).strip()
                if len(m.group(2)) > 0:
                    self._apply_quantity_to_others = True
                    
                successed = True
                
        if not successed:#quantity
            m = re.compile(quantity_unit_pattern).match(text)
            if m:
                successed = True
                self._quantity_unit = m.group(1).strip()
                successed = True
                
        if not successed:#comment
            m = re.compile(comment_pattern).match(text)
            if m:
                self._comments = m.group(1).strip()
    
    def __parse_normal_medical_name__(self):
        pattern = ur"([^（）一二三四五六七八九十半百各]+)(\W*)"
        m = re.compile(pattern).match(self._source_text)
        if m:
            self._herb = m.group(1).strip()
            self.__parse_quantity_comment__(m.group(2).strip())

    def get_component(self):   
        m = MedicalNameParser(self._source_text)
        herb, other = m.split_with_medical_name()
        if herb:
            self._herb = herb
            self.__parse_quantity_comment__(other)
        else:
            self.__parse_normal_medical_name__()
        
        quantity, unit = (None, None)
        if self._quantity_unit:
            quantity_parser = QuantityParser(self._quantity_unit)
            quantity, unit = quantity_parser.parse()
         
        component = {'medical': self._herb, 'quantity': quantity, 'unit': unit, 'comments': self._comments, 
                     "applyQuantityToOthers":self._apply_quantity_to_others} 
        
        if self._component_adjustor:
            component = self._component_adjustor.adjust(component)
            
        
        print Utility.convert_dict_to_string(component)
        return component
    

if __name__ == "__main__": 
    def test():
        texts = [u'制附片60克(久煎)',
                 u'制附片60克',
                 u'制附片60']     
     
        for item in texts:
            print item + " "
            sp = SingleComponentParser1(item)
            component = sp.get_component()
            print Utility.convert_dict_to_string(component)
            
    test()   
    print "done"