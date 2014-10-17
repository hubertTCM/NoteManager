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

def adjust_components(getComponents):
    def inner(*args, **kwargs):
        components = getComponents(*args, **kwargs)
        components.reverse() #防风　桔梗　桂枝　人参　甘草各一两
        previous_quantity = 0
        previous_unit = None
        for component in components:#{'quantity': quantity, 'medical': medical, 'unit': unit, 'comments': comments}
            apply_quantity_to_others = Utility.get_bool_value('applyQuantityToOthers', component)
            if apply_quantity_to_others:
                previous_quantity = component['quantity']
                previous_unit = component['unit']
            else:
                if component['quantity'] == 0: 
                    if previous_quantity > 0:
                        component['quantity'] = previous_quantity
                        component['unit'] = previous_unit
                else:
                    previous_quantity = 0
                    previous_unit = None
        components.reverse()
        return components
    return inner

#制附片60克(久煎) 
#葱白60克 
class ComponentParser1:
    def __clear__(self):
        self._source_text = None
        self._herb = None
        self._quantity_unit = None
        self._apply_quantity_to_others = False
        self._comments = None 
        
    def __parse_quantity_comment__(self, text):
        quantity_unit_pattern = ur"([各]?[\d]+[.]?[\d]*[^（(]+)"
        comment_pattern = ur"[（(]([\W]+)[)）]"
        successed = False
        # quantity（comment）
        m = re.compile(quantity_unit_pattern + comment_pattern).match(text)
        if m:
            self._quantity_unit = m.group(1).strip()
            self._comments = m.group(2).strip()
            successed = True
            
        if not successed:#（comment）quantity
            m = re.compile(comment_pattern + quantity_unit_pattern).match(text)
            if m:
                self._quantity_unit = m.group(2).strip()
                self._comments = m.group(1).strip()
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
                
        if self._quantity_unit and self._quantity_unit[:1] == u"各":
            self._quantity_unit = self._quantity_unit[1:]
            self._apply_quantity_to_others = True
    
    def __parse_normal_medical_name__(self):
        pattern = ur"([^（）()\d各]+)([\d.\W]*)"
        m = re.compile(pattern).match(self._source_text)
        if m:
            self._herb = m.group(1).strip()
            self.__parse_quantity_comment__(m.group(2).strip())

    def getComponent(self, text):
        self.__clear__()
        self._source_text = text
        self._herb = text
           
        m = MedicalNameParser(self._source_text)
        herb, other = m.split_with_medical_name()
        if herb:
            self._herb = herb
            self.__parse_quantity_comment__(other)
        else:
            self.__parse_normal_medical_name__()
        
        quantity, unit = (0, None)
        if self._quantity_unit:
            quantityParser = QuantityParser1(self._quantity_unit)
            quantity, unit = quantityParser.parse()
         
        component = {'medical': self._herb, 'quantity': quantity, 'unit': unit, 'comments': self._comments, 
                     "applyQuantityToOthers":self._apply_quantity_to_others} 
        return component

class ComponentParser2:
    def __init__(self, text, component_adjustor):
        self._source_text = text
        self._herb = text
        self._quantity_unit = None
        self._apply_quantity_to_others = False
        self._comments = None 
        self._component_adjustor = component_adjustor
        
    def __parse_quantity_comment__(self, text):
        quantity_unit_pattern = ur"([各]?[一二三四五六七八九十半百]+[^（(]+)"
        comment_pattern = ur"[（(]([\W]+)[)）]"
        successed = False
        # quantity（comment）
        m = re.compile(quantity_unit_pattern + comment_pattern).match(text)
        if m:
            self._quantity_unit = m.group(1).strip()
            self._comments = m.group(2).strip()
            successed = True
            
        if not successed:#（comment）quantity
            m = re.compile(comment_pattern + quantity_unit_pattern).match(text)
            if m:
                self._quantity_unit = m.group(2).strip()
                self._comments = m.group(1).strip()                    
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
        
        
        if self._quantity_unit and self._quantity_unit[:1] == u"各":
            self._quantity_unit = self._quantity_unit[1:]
            self._apply_quantity_to_others = True
            
    
    def __parse_normal_medical_name__(self):
        pattern = ur"([^（）()一二三四五六七八九十半百]+)(\W*)"
        m = re.compile(pattern).match(self._source_text)
        if m:
            self._herb = m.group(1).strip()
            self.__parse_quantity_comment__(m.group(2).strip())

    def getComponent(self):   
        m = MedicalNameParser(self._source_text)
        herb, other = m.split_with_medical_name()
        if herb:
            self._herb = herb
            self.__parse_quantity_comment__(other)
        else:
            self.__parse_normal_medical_name__()
        
        quantity, unit = (0, None)
        if self._quantity_unit:
            quantity_parser = QuantityParser2(self._quantity_unit)
            quantity, unit = quantity_parser.parse()
         
        component = {'medical': self._herb, 'quantity': quantity, 'unit': unit, 'comments': self._comments, 
                     "applyQuantityToOthers":self._apply_quantity_to_others} 
        
        if self._component_adjustor:
            component = self._component_adjustor.adjust(component)
            
        
        print Utility.convert_dict_to_string(component)
        return component
    
class PrescriptionParser1:
    def __init__(self, splitTags, sourceText, componentParser):
        self.__splitTags__ = splitTags
        self.__sourceText__ = sourceText
        self.__componentParser__ = componentParser
        
    @adjust_components
    def getComponents(self):
        toTag = self.__splitTags__[0]
        for tag in self.__splitTags__:
            if tag == toTag:
                continue
            self.__sourceText__ = self.__sourceText__.replace(tag, toTag)
            
        items = (filter(lambda(x) : len(x) > 0, [item.strip() for item in self.__sourceText__.split(toTag)]))
        if len(items) <= 0:
            return None
        
        components = []
        
        for item in items:
            item = item.strip()
            if len(item) > 0:
                components.append(self.__componentParser__.getComponent(item))
                
        if (len(components) == 0):
            print "*failed to get components from: " + self.__sourceText__ + '\n'
            
        return components

class PrescriptionQuantityFilter1:    
    def splitByQuantity(self, text):
        otherText = text
        quantity = 0
        unit = None
        
        text = text.strip()
        
        pattern = ur"([一二三四五六七八九十]+[剂付])"
        m = re.compile(pattern).search(text)
        if m:
            otherText = text[:m.start()]
#             otherText = m.group(1)
            quantityParser = QuantityParser2(text[m.start():])
            quantity, unit = quantityParser.parse()
        return quantity, unit, otherText
    
if __name__ == "__main__": 
    def test1():
        texts = [u'童便(为引)',
                 u'麻黄10克',
                 u'制附片各3.5克',
                 u'制附片60克(久煎)',
                 u'制附片60克',
                 u'制附片60']     
       
        sp = ComponentParser1()
        for item in texts:
            print item + " "
            component = sp.getComponent(item)
            print Utility.convert_dict_to_string(component)
            
        text = u'童便(为引) 桂枝10克  白芍1O克  炙甘草6克  生姜6克  大枣10枚  白薇12克  三剂 '
        #text = u' 桂枝6克  麻黄10克  甘草18克  杏仁15克  二剂'
        filter1 = PrescriptionQuantityFilter1()
        quantity, unit, componentsText = filter1.splitByQuantity(text)
        parser1 = PrescriptionParser1([' '], componentsText, ComponentParser1())
        print "quantity:" + str(quantity) + " unit:" + unit
        for component in parser1.getComponents():
            print Utility.convert_dict_to_string(component)
    test1()   
    print "done"