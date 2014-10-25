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
from ConsiliaUtility import *

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
		
		self.__source__ = { u'comeFrom': {'bookTitle':u'赵绍琴临证验案精选'}, u'author':u'赵绍琴' }
		
		self.__componentsParser__ = ComponentsParser1(['，', '、'], SingleComponentParser1())
		self.__prescriptionParser__ = PrescriptionParser1(self.__componentsParser__)
		
		
		comment_key_words = [ur"水煎服", 
							ur"连服([两一二三四五六七八九十]+[剂付])", #连服三付而愈,
							ur"连服[\d]+[剂付]",  #连服三付而愈
							ur"服上方[一二三四五六七八九十]+[剂付]", #服上方三剂
							
							ur"又服[一二三四五六七八九十]+[剂付]",#又服三付而愈
							ur"又服[\d]+[剂付]",#又服三付而愈
							
							ur"上方去", #上方去大黄、川楝子、大腹皮、槟榔，7剂
							ur"\W*原方继进"#药后痛止眠安，仍以前法进退。忌食辛辣肥甘为要。原方继进10剂。
							]
		self.__comment_patterns__ = []
		for key_word in comment_key_words:
			self.__comment_patterns__.append( re.compile(ur"^[ ]*"+ key_word))
			
		self.__disease_name_pattern__ = re.compile(ur" *([^ ]+) +[一二三四五六七八九十]*")
		
		self.__description_patterns__ = []
		description_words = [ur"【初诊】"]
		for key_word in description_words:
			self.__description_patterns__.append(re.compile(ur"^ *"+ key_word))
		self.__description_patterns__.append(re.compile(ur"前药服后"))
		self.__description_patterns__.append(re.compile(ur"^ *[^某]+某 *，*[男女] *，\d+岁")) #吕某，男，45岁
		self.__description_patterns__.append(re.compile(ur"诊断：")) #诊断：肠伤寒。
		
	def __is_description__(self, line):
		for pattern in self.__description_patterns__:
			if pattern.search(line):
				return True
		return False
		
	def __get_prescription__(self, line):
# 		comment_key_words = [ur"水煎服", 
# 							ur"连服([两一二三四五六七八九十]+[剂付])", #连服三付而愈,
# 							ur"连服[\d]+[剂付]",  #连服三付而愈
# 							ur"服上方[一二三四五六七八九十]+[剂付]", #服上方三剂
# 							ur"上方去", #上方去大黄、川楝子、大腹皮、槟榔，7剂
# 							ur"\W*原方继进"#药后痛止眠安，仍以前法进退。忌食辛辣肥甘为要。原方继进10剂。
# 							]
# 		for key_word in comment_key_words:
# 			if re.compile(ur"^[ ]*"+ key_word).search(line):
# 				return None

		for pattern in self.__comment_patterns__:
			if pattern.search(line):
				return None

		return self.__prescriptionParser__.getPrescription(line)
	
	def __extract_disease_names__(self, text):
		names = []
		for item in text.split(u'、'):
			m = self.__disease_name_pattern__.match(item)
			if m:
				names.append(m.group(1))
			else:
				names.append(item.strip())
		return names
		
	def getAll(self):			
		sourceFile = codecs.open(self.__filePath__, 'r', 'utf-8', 'ignore')
		
		yiAnSplitPattern = re.compile(ur"^【[复二三四五六七八九十]+诊】[:: ]*")
		yiAn_comment_pattern = re.compile(ur"^【按】")
		items = []
		
		is_comment = False
		currentYiAn = None
		currentCategory = None
		currentName = None
		currentDetail = None
		order = 1
		
		def createDetail(order):
			return {"description" : "", "order" : order, 'prescriptions':[], 'comment':""}

		for line in sourceFile.readlines():
			line = line.strip(" \t\r\n")
			if len(line) == 0:
				if currentYiAn and len(currentYiAn['diseaseNames']) > 0:
					currentYiAn["details"].append(currentDetail)
					items.append(currentYiAn)
				
				order = 1
				currentYiAn = {'diseaseNames':[], "details":[]}
				currentName = None
				currentDetail = createDetail(order)
				continue
			
			if line in self.__categories__:
				currentCategory = line
				is_comment = False
				continue
			
			if not currentName:
				is_comment = False
				currentYiAn['diseaseNames'].append(currentCategory)
				
				if self.__is_description__(line):
					currentName = currentCategory
					currentDetail['description'] += "\n" + line
					continue
				
				currentName = line
				currentYiAn['diseaseNames'].extend(self.__extract_disease_names__(line))
				continue
			
			m = yiAnSplitPattern.search(line)
			if m:
				is_comment = False
				currentYiAn["details"].append(currentDetail)
				order += 1
				currentDetail = createDetail(order)
				currentDetail['description'] += "\n" + line
				continue
			
			if self.__is_description__(line):
				is_comment = False
				currentDetail['description'] += "\n" + line
				continue
			
			if yiAn_comment_pattern.search(line):
				is_comment = True
				currentDetail['comment'] += "\n" + line
				continue
			
			if is_comment:
				currentDetail['comment'] += "\n" + line
				continue
				
			prescription = self.__get_prescription__(line)#self.__prescriptionParser__.getPrescription(line)
			if prescription:
				currentDetail['prescriptions'].append(prescription)
				continue
			
			if len(currentDetail['prescriptions']) == 0:
				currentDetail['description'] += "\n" + line
				continue
			
			currentDetail['comment'] += "\n" + line
			
			sourceFile.close()
		
		for yiAn in items:
			yiAn.update(self.__source__)
			for item in yiAn['details']:
				item['description'] = item['description'].strip(" \n")
				item['comment'] = item['comment'].strip(" \n")
		
		return items

if __name__ == "__main__":
	provider = Provider_zsq()
	provider.__get_prescription__(ur"水煎服，每日一剂。")
	Updater().update(provider.__filePath__)
	items = provider.getAll()		
	writer = ConsiliaWriter()
	writer.write_consilias(items)
	
	h = ConsiliaHelper()
	herbs = h.get_un_imported_herbs(items)
	logger = Logger()
	logger.write_lines(herbs)
	logger.write_line("unit")
	logger.write_lines(h.get_units(items))
	logger.write_line("prescription name")
	logger.write_lines(h.get_prescritpion_names(items))

# 	herbs = []
# 	def shouldPrint(prescription):
# 		return True
# 		for component in prescription['components']:
# 			if component["quantity"] == 0:
# 				return True
# 		return False
# 	detailDefault = {u'description' : "None", "comment" : "None"}
# 	for item in items:
# 		file_writer.write(" ".join(item['diseaseNames']) + "\n")
# 		for detail in item['details']:
# 			Utility.apply_default_if_not_exist(detail, detailDefault)
# # 			file_writer.write("index:" + str(detail[u'order']) + "\n")
# # 			file_writer.write("description:" + detail[u'description'] + "\n")
# # 			file_writer.write("comment:" + detail[u'comment'] + "\n")
# 
# #			file_writer.write(detail[u'description'] + "\n")
# # 			file_writer.write("\n")
# # 			file_writer.write(detail[u'diagnosis'] + "\n")
# # 			file_writer.write("\n")
# # 			file_writer.write(detail[u'comments'] + "\n")
# # 			file_writer.write("\n")
# #			for prescription in detail['prescriptions']:
# # 				if not shouldPrint(prescription):
# # 					continue
# #				file_writer.write(prescription["name"] + "\n")
# 				#if 'components' in prescription:
# # 				for component in prescription['components']:
# # 					if component['applyQuantityToOthers']:
# # 						if not component['medical'] in herbs:
# # 							herbs.append(component['medical'])
# 				#file_writer.write(Utility.convert_dict_to_string(component)+ "\n") 
# # 				file_writer.write(str(prescription["quantity"]) + " " + prescription["unit"] + "\n")
# # 				file_writer.write(prescription["comment"] + "\n")
# 				#file_writer.write(prescription['_debug'] + "\n")
# 			#file_writer.write(detail[u'comment'] + "\n")
# # 	i = 0
# # 	file_writer.write("items.update({")
# # 	for herb in herbs:
# # 		file_writer.write("ur\"" + herb + "\" : " + "ur\"" + herb[0] + herb[2:] + " " + herb[1:] + "\",  ")
# # 		i += 1
# # 		if i == 3:
# # 			i = 0
# # 			file_writer.write("})")
# # 			file_writer.write("\n")
# # 			file_writer.write("items.update({")
# # 	
# # 	file_writer.write("})")
# 	file_writer.close()
	print "done"
