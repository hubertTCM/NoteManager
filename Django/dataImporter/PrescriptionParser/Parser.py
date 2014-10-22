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
        
        if not components:
            return components
        
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
class SingleComponentParser1:
    def __clear__(self):
        self._source_text = None
        self._herb = None
        self._quantity_unit = None
        self._apply_quantity_to_others = False
        self._comments = None 
        
    def __parse_quantity_comment__(self, text):
        quantity_unit_pattern = ur"([各]?[\d]+[.]?[\d]*[^（(]+)"
        comment_pattern = ur"[（(]([\W\d.]+)[)）]"
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
           
#         m = MedicalNameParser(self._source_text)
#         herb, other = m.split_with_medical_name()
#         if herb:
#             self._herb = herb
#             self.__parse_quantity_comment__(other)
#         else:
        self.__parse_normal_medical_name__()
        
        quantity, unit = (0, None)
        if self._quantity_unit:
            quantityParser = QuantityParser1(self._quantity_unit)
            quantity, unit = quantityParser.parse()
         
        component = {'medical': self._herb, 'quantity': quantity, 'unit': unit, 'comments': self._comments, 
                     "applyQuantityToOthers":self._apply_quantity_to_others} 
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
    
class ComponentsParser1:
    def __init__(self, splitTags, componentParser):
        self.__splitTags__ = splitTags
        self.__componentParser__ = componentParser
        
    @adjust_components
    def getComponents(self, sourceText):
        self.__sourceText__ = sourceText
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

class NameCommentSpliter1:
    def __init__(self):
        self.__nameCommentPattern__ = re.compile(ur"(^[^（(:：]+)[（(]([\W]+)[)）][:：][ ]*")
        self.__namePattern__ = re.compile(ur"(^[^（(:：]+)[:：][ ]*")
        
    def split(self, text):
        m = self.__nameCommentPattern__.match(text)
        name = ""
        comment = ""
        other = text
        if m:
            name = m.group(1)
            comment = m.group(2)
            other = text[m.end():]
            return name, comment, other
        
        m = self.__namePattern__.match(text)
        if m:
            name = m.group(1)
            other = text[m.end():]
        return name, comment, other

class PrescriptionParser1:
    def __init__(self, componentsParser):
        self.__componentsParser__ = componentsParser
        self.__nameCommentParser__ = NameCommentSpliter1()
        
        quantityPattern = ur"([服]*[一二三四五六七八九十]+[剂付])[。]*$"
        self.__quantityPattern__ = re.compile(quantityPattern)
        
        quantityCommentPattern = ur"([服]*[一二三四五六七八九十]+[剂付])[。]*[（(]([\W]+)[)）]$"
        self.__quantityCommentPattern__ = re.compile(quantityCommentPattern)
        
    def getPrescription(self, text):
        text = text.strip()
        
        m = self.__quantityPattern__.search(text)
        comment = None
        if not m:
            m = self.__quantityCommentPattern__.search(text)
            if m:
                comment = m.group(2)
            
        if m:
            quantityParser = QuantityParser2(m.group(1))
            quantity, unit = quantityParser.parse()
            otherText = text[:m.start()]
            
            item = self.__nameCommentParser__.split(otherText)
            if not comment:
                comment = item[1]
                
            prescription = {"name": item[0], "comment":comment, "quantity" : quantity, "unit" : unit, "_debug":text}
            components = self.__componentsParser__.getComponents(item[2])
            
            if components:
                prescription['components'] = components
                return prescription
        return None

if __name__ == "__main__": 
    def outputPrescription(prescription):
        print "name:" + prescription['name']+ " quantity:" + str(prescription['quantity']) + " unit:" + prescription['unit']
        for component in prescription['components']:
            print Utility.convert_dict_to_string(component)
        print "comment:" + prescription['comment']
        
    def test1():
#         texts = [u'童便(为引)',
#                  u'麻黄10克',
#                  u'制附片各3.5克',
#                  u'制附片60克(久煎)',
#                  u'制附片60克',
#                  u'制附片60']     
#        
#         sp = SingleComponentParser1()
#         for item in texts:
#             print item + " "
#             component = sp.getComponent(item)
#             print Utility.convert_dict_to_string(component)
#             
#         text = u'童便(为引) 桂枝10克  白芍1O克  炙甘草6克  生姜6克  大枣10枚  白薇12克  三剂 '
#         #text = u' 桂枝6克  麻黄10克  甘草18克  杏仁15克  二剂'
#         filter1 = PrescriptionQuantityFilter1()
#         quantity, unit, componentsText = filter1.splitByQuantity(text)
#         parser1 = ComponentsParser1([' '], SingleComponentParser1())
#         print "quantity:" + str(quantity) + " unit:" + unit
#         for component in parser1.getComponents(componentsText):
#             print Utility.convert_dict_to_string(component)
        
        texts =[ur"生石膏30克(先煎)，知母15克，生甘草10克，梗米30克，生黄芪30克，五味子10克，西洋参粉6克，一付(即刻先服)", 
                ur"麦门冬10克，沙参10克，五味子6克，蝉衣6克，僵蚕10克，片姜黄6克，柴胡6克，黄芩6克，白芍10克，丝瓜络，桑枝， 七剂",
                 ur"处方二： 鲜九节菖蒲根15克（煎汤送服神犀丹一丸 犀角末0.6克 分二次汤药送下） 一付。",
                 ur"处方：生白芍15克，天麦冬各6克，沙参20克，元参15克，石斛10克，前胡6克，黄芩10克，杏仁10克，黛蛤散12克(包)，川贝粉3克(冲)，羚羊角粉0.5克(冲)，服二剂"
                 ]
        componentsParser = ComponentsParser1(['，'], SingleComponentParser1())
        prescriptionParser = PrescriptionParser1(componentsParser)
        for text in texts:
            prescription = prescriptionParser.getPrescription(text)
            outputPrescription(prescription)
    test1()   
    print "done"