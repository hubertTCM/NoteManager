# -*- coding: utf-8 -*-
import sys
import os
import codecs
import re

def append_ancestors_to_system_path(levels):
	parent = os.path.dirname(__file__)
	for i in range(levels):
		sys.path.append(parent)
		parent = os.path.abspath(os.path.join(parent, ".."))

append_ancestors_to_system_path(3)

from dataImporter.Utils.Utility import *
from dataImporter.PrescriptionParser.Parser import *
from ConsiliaFileUpdater import Updater

#TBD
class Provider_zsq:	
	def __init__(self):
		self.__filePath__ = os.path.dirname(__file__) + ur'\resources\赵绍琴临证验案精选.txt'
		pattern = ur"(处方[一二三四五六七八九十]*)[:：；][ ]*([^处方]*)"
		self.__prescritionNamePattern__ = re.compile(pattern)
		
		self.__categories__ = [ur"风温",ur"春温",ur"暑温",ur"湿阻",ur"凉遏",ur"寒凝",ur"冰伏",ur"湿温",ur"伏暑",ur"肺炎"]
		self.__categories__.extend([ur"秋燥",ur"冬温",ur"春温",ur"痄腮", ur"烂喉痧", ur"温毒", ur"昏迷"])
		self.__categories__.extend([ur"麻疹", ur"肺痈", ur"咳嗽", ur"咳喘", ur"咳血", ur"失音", ur"鼻鼽", ur"鼻痔", ur"胃脘痛"])
		self.__categories__.extend([ur"胁痛", ur"腹痛",ur"呕吐",ur"中暑",ur"痢疾",ur"泄泻"])
		self.__categories__.extend([ur"便秘",ur"眩晕",ur"头痛",ur"心悸",ur"胸痛",ur"嗜睡",ur"失眠",ur"耳聋",ur"癫痫",ur"振颤"])
		self.__categories__.extend([ur"发斑",ur"齿衄",ur"鼻衄",ur"臌胀",ur"消渴",ur"黑疸",ur"肥胖",ur"阳痿",ur"阳强",ur"痹证"])
		self.__categories__.extend([ur"淋证",ur"遗尿",ur"尿血",ur"水肿",ur"关格",ur"腰痛",ur"尿浊",ur"喘逆",ur"崩漏",ur"闭经"])
		self.__categories__.extend([ur"头汗",ur"脱发",ur"牙疳",ur"白疙",ur"头疮",ur"赘疣"])
		self.__categories__.extend([ur"癌", ur"瘿", ur"皮肤搔痒", ur"经期发热"])
		
		self.__source__ = { u'comeFrom': u'赵绍琴临证验案精选', u'author':u'赵绍琴' }
		
		self.__componentsParser__ = ComponentsParser1(['，'], SingleComponentParser1())
		self.__prescriptionParser__ = PrescriptionParser1(self.__componentsParser__)
		
	def getAll(self):			
		sourceFile = codecs.open(self.__filePath__, 'r', 'utf-8', 'ignore')
		
		yiAnSplitPattern = re.compile(ur"【[复二三四五六七八九十]+诊】[:: ]*$")
		#commentPattern = re.compile(ur"【[原]*按】[:: ]*")
		
		items = []
		
		currentYiAn = None
		currentCategory = None
		currentName = None
		currentDetail = None
		order = 1
		
		def createDetail(order):
			return {"description" : "", "order" : order, 'prescriptions':[], 'comment':""}

		for line in sourceFile.readlines():
			line = line.strip(" \r\n")
			if len(line) == 0:
				if currentYiAn:
					currentYiAn["details"].append(currentDetail)
					items.append(currentYiAn)
				
				order = 1
				currentYiAn = {'diseaseNames':[], "details":[]}
				currentName = None
				currentDetail = createDetail(order)
				continue
			
			if line in self.__categories__:
				currentCategory = line
				continue
			
			if not currentName:
				currentName = line
				currentYiAn['diseaseNames'].append(currentCategory)
				currentYiAn['diseaseNames'].extend(filter(lambda(x):len(x) > 0, [item.strip() for item in line.split(u'、')]))
				continue
			
			m = yiAnSplitPattern.match(line)
			if m:
				currentYiAn["details"].append(currentDetail)
				
				order += 1
				currentDetail = createDetail(order)
				currentDetail['description'] += "\n" + line
				continue
			
			prescription = self.__prescriptionParser__.getPrescription(line)
			if prescription:
				currentDetail['prescriptions'].append(prescription)
				continue
			
			
			if len(currentDetail['prescriptions']) == 0:
				currentDetail['description'] += "\n" + line
				continue
			
			currentDetail['comment'] += "\n" + line
			continue
			
			sourceFile.close()
		
		for yiAn in items:
			for item in yiAn['details']:
				item['description'].strip(" \n")
				item['comment'].strip(" \n")
				item.update(self.__source__)
		
		return items

if __name__ == "__main__":
	provider = Provider_zsq()
	Updater().update(provider.__filePath__)
	items = provider.getAll()	
	to_file = os.path.dirname(__file__) + '\\debug.txt'
	file_writer = codecs.open(to_file, 'w', 'utf-8', 'ignore')
	

	herbs = []
	def shouldPrint(prescription):
		return True
		for component in prescription['components']:
			if component["quantity"] == 0:
				return True
		return False
	detailDefault = {u'description' : "None", u'comments' : "None", "diagnosis" : "None", "comment" : "None"}
	for item in items:
#		file_writer.write(" ".join(item['diseaseNames']) + "\n")
		for detail in item['details']:
			Utility.apply_default_if_not_exist(detail, detailDefault)
# 			file_writer.write("index:" + str(detail[u'order']) + "\n")
# 			file_writer.write("description:" + detail[u'description'] + "\n")
# 			file_writer.write("diagnosis:" + detail[u'diagnosis'] + "\n")
#  			file_writer.write("comments:" + detail[u'comments'] + "\n")

#			file_writer.write(detail[u'description'] + "\n")
# 			file_writer.write("\n")
# 			file_writer.write(detail[u'diagnosis'] + "\n")
# 			file_writer.write("\n")
# 			file_writer.write(detail[u'comments'] + "\n")
# 			file_writer.write("\n")
			for prescription in detail['prescriptions']:
				if not shouldPrint(prescription):
					continue
#				file_writer.write(prescription["name"] + "\n")
				#if 'components' in prescription:
				for component in prescription['components']:
					if component['applyQuantityToOthers']:
						if not component['medical'] in herbs:
							herbs.append(component['medical'])
				#file_writer.write(Utility.convert_dict_to_string(component)+ "\n") 
# 				file_writer.write(str(prescription["quantity"]) + " " + prescription["unit"] + "\n")
# 				file_writer.write(prescription["comment"] + "\n")
				#file_writer.write(prescription['_debug'] + "\n")
			#file_writer.write(detail[u'comment'] + "\n")
	i = 0
	file_writer.write("items.update({")
	for herb in herbs:
		file_writer.write("ur\"" + herb + "\" : " + "ur\"" + herb[0] + herb[2:] + " " + herb[1:] + "\",  ")
		i += 1
		if i == 3:
			i = 0
			file_writer.write("})")
			file_writer.write("\n")
			file_writer.write("items.update({")
	
	file_writer.write("})")
	file_writer.close()
	print "done"
