# -*- coding: utf-8 -*-
import os
import re
import sys
from dataImporter.prescriptionImporter import herbUtility


def append_ancestors_to_system_path(levels):
    parent = os.path.dirname(__file__)
    for i in range(levels):
        sys.path.append(parent)
        parent = os.path.abspath(os.path.join(parent, ".."))
        
append_ancestors_to_system_path(3)

from dataImporter.ConsiliaProvider.ConsiliaUtility import *
from dataImporter.Utils.Utility import *
from dataImporter.Utils.HerbUtil import *
from ComponentAdjustor import *

herbUtility = HerbUtility() 

def convert_name(from_name):
    items = [ur"药用", ur"方用", ur"处方", ur"拟方如下", ur"方药"]
    
    for item in items:
        if from_name.startswith(item):
            return from_name[len(item):]
    
    return from_name

def adjust_components(getComponents):
    def inner(*args, **kwargs):
        components = getComponents(*args, **kwargs)
        
        if not components:
            return components
        
        components.reverse() #防风　桔梗　桂枝　人参　甘草各一两
        previous_quantity = 0
        previous_unit = None
        for component in components:#{'quantity': quantity, 'medical': medical, 'unit': unit, 'comments': comments}
            component['medical'] = convert_name(component['medical'])
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
        self.__parse_normal_medical_name__()
        
        quantity, unit = (0, None)
        if self._quantity_unit:
            quantityParser = QuantityParser1()
            quantity, unit = quantityParser.parse(self._quantity_unit)
         
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
    def __init__(self):
        self.__quantity_parser__ = QuantityParser2()
          
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
            #quantityParser = QuantityParser2()
            quantity, unit = self.__quantity_parser__.parse(text[m.start():])
        return quantity, unit, otherText

class NameCommentSpliter1:
    def __init__(self):
        self.__nameCommentPattern__ = re.compile(ur"(^[^（(:：；]+)[（(]([\W]+)[)）][:：；][ ]*")
        self.__namePattern__ = re.compile(ur"(^[^（(:：；]+)[:：；][ ]*")
        
    def split(self, text):
        m = self.__nameCommentPattern__.match(text)
        name = ""
        comment = ""
        other = text
        if m:
            name = m.group(1)
            comment = m.group(2)
            other = text[m.end():]
            return convert_name(name), comment, other
        
        m = self.__namePattern__.match(text)
        if m:
            name = m.group(1)
            other = text[m.end():]
        return convert_name(name), comment, other

class PrescriptionParser1:
    def __init__(self, componentsParser):
        self.__componentsParser__ = componentsParser
        self.__nameCommentParser__ = NameCommentSpliter1()
        
        quantityPatterns = [ur"服*([一二三四五六七八九十]+[剂付])",
                            ur"服*([\d]+[剂付])"]
        postItem = ur"(而愈|，煎服|，水煎服|。水煎服|，巩固疗效)*[。]?$"
        self.__quantity_patterns__ = [re.compile(item + postItem) for item in quantityPatterns]
        self.__ignore_quantity_patterns__ = []
        self.__ignore_quantity_patterns__.insert(0, re.compile(ur"水煎服，每日([\d]+[剂付])[。]?$"))
        self.__ignore_quantity_patterns__.insert(0, re.compile(ur"水煎服，每日([一二三四五六七八九十]+[剂付])[。]?$"))
        quantityCommentPatterns = [ur"([服]*[一二三四五六七八九十]+[剂付])[。]*[（(]([\W\d]+)[)）]$",
                                   ur"([服]*[\d]+[剂付])[。]*[（(]([\W\d]+)[)）]$"]
        self.__quantityCommentPatterns__ = [re.compile(item) for item in quantityCommentPatterns]
        
        self.__quantityParsers__ = [QuantityParser1(), QuantityParser2()]
        
    def __parse_without_quantity__(self, text, check_medical):
        name, comment, componentsText = self.__nameCommentParser__.split(text)
        components = self.__componentsParser__.getComponents(componentsText)
        if not components:
            return None
        
        #contains_unknown_herb = False
        contains_unkown_herb = False
        contains_unkown_quantity = False
        if check_medical:
            for component in components:
                if not herbUtility.isHerb(component['medical']):
                    contains_unkown_herb = True
                if component['quantity'] == 0:
                    contains_unkown_quantity = True
            if contains_unkown_herb and contains_unkown_quantity:
                return None
        return {"name": convert_name(name), "comment":comment, "quantity" : 0, "unit" : "", "components": components, "_debug":text}
            
    def getPrescription(self, text):
        m = None
        
        text = text.strip()
        for pattern in self.__ignore_quantity_patterns__:
            m = pattern.search(text) 
            if m:
                return self.__parse_without_quantity__(text[:m.start()], False)

        for pattern in self.__quantity_patterns__:
            m = pattern.search(text)
            if m:
                break
            
        comment = None
        if not m:
            for pattern in self.__quantityCommentPatterns__:
                m = pattern.search(text)
                if m:
                    comment = m.group(2)
                    break
            
        if m:
            quantity = 0
            unit = ""
            for parser in self.__quantityParsers__:
                quantity, unit = parser.parse(m.group(1))
                if quantity > 0 and unit and len(unit) > 0:
                    break
            otherText = text[:m.start()]
            
            item = self.__nameCommentParser__.split(otherText)
            if not comment:
                comment = item[1]
                
            prescription = {"name": convert_name(item[0]), "comment":comment, "quantity" : quantity, "unit" : unit, "_debug":text}
            components = self.__componentsParser__.getComponents(item[2])
            
            if components:
                prescription['components'] = components
                return prescription
            
        return self.__parse_without_quantity__(text, True)

if __name__ == "__main__": 
    writer = PrescriptionWriter()
    writer.create()
    def outputPrescription(prescription):
        writer.write_single_prescription(prescription)
#         if not prescription:
#             print "None"
#             return
#         print "name:" + prescription['name']+ " quantity:" + str(prescription['quantity']) + " unit:" + prescription['unit']
#         for component in prescription['components']:
#             print Utility.convert_dict_to_string(component)
#         print "comment:" + prescription['comment']
        
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
        
        texts =[ur" 拟方如下：荆芥炭、防风、佩兰、藿香、生地愉、炒槐花、丹参、茜草、白鲜皮、地肤子、草河车、大腹皮、槟榔、灶心土、大黄，水煎服，每日一剂。",
                ur"药用:蝉蜕3克，僵蚕6克，片姜黄3克，大黄1克，白茅根10克，小蓟10克，生地榆6克，炒槐花6克，茜草6克，水煎服，每日1剂。",
                ur"荆芥，防风，白芷，独活，生地榆，炒槐花，丹参，茜草，焦三仙，水红花子，大腹皮，槟榔，大黄",
                ur"处方；藿香10克，佩兰10克，苏叶10克，茅芦根各10克，3剂（少量多次服用）",
                ur"方用：蝉衣、青黛(冲)、片姜黄各6克，大黄2克，生地榆、赤芍、丹参、茜草、小蓟、半枝莲、白花蛇舌草各10克。",
                ur"焦三仙各150克，鸡内金150克，砂仁3克",
                ur"药用：陈皮10克，防风6克，白术10克，白芍10克，葛根10克，黄芩10克，黄连3克，荆芥炭10克，灶心土30克，7剂，水煎服。",
                ur"荆芥6克，防风6克，生地榆10克，赤芍10克，丹参10克，茜草10克，茅芦根各10克，焦三仙各10克，水红花子10克，七剂。水煎服。",
                ur"柴胡6克，黄芩10克，川楝子10克，蝉衣6克，僵蚕10克，片姜黄10克，竹茹6克，枳壳6克，焦三仙各10克，七剂，水煎服。",
                ur"黄连2克，蝉衣6克，僵蚕10克，复盆子10克，钩藤10克，川楝子6克，生牡蛎20克，7剂，巩固疗效。",
                ur"桂枝10克，干姜6克，香薷6克，半夏10克，厚朴6克，草蔻3克，炒川椒6克，生姜6克，一付，煎服",
                ur"苏藿梗各6克，半夏曲10克，陈皮6克，厚朴花6克，白莲仁3克，鲜煨姜3克，焦麦芽10克，二付而愈。",
                ur"药用：前胡6克，杏仁10克，浙贝母10克，枇杷叶10克，荆芥炭10克，防风6克，白茅根10克，芦根20克，木通色克，扁蓄10克，冬葵子20克，大黄1克，独活6克，生地榆10克。",
                ur"生石膏30克(先煎)，知母15克，生甘草10克，梗米30克，生黄芪30克，五味子10克，西洋参粉6克，一付(即刻先服)", 
                ur"麦门冬10克，沙参10克，五味子6克，蝉衣6克，僵蚕10克，片姜黄6克，柴胡6克，黄芩6克，白芍10克，丝瓜络，桑枝， 七剂",
                 ur"处方二： 鲜九节菖蒲根15克（煎汤送服神犀丹一丸 犀角末0.6克 分二次汤药送下） 一付。",
                 ur"处方：生白芍15克，天麦冬各6克，沙参20克，元参15克，石斛10克，前胡6克，黄芩10克，杏仁10克，黛蛤散12克(包)，川贝粉3克(冲)，羚羊角粉0.5克(冲)，服二剂"
                 ]
        componentsParser = ComponentsParser1(['，', '、'], SingleComponentParser1())
        prescriptionParser = PrescriptionParser1(componentsParser)
        for text in texts:
            prescription = prescriptionParser.getPrescription(text)
            outputPrescription(prescription)
    test1()   
    print "done"