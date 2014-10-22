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

class Provider_fzl:	
	def __init__(self):
		self._source_file_fullpath = os.path.dirname(__file__) + '\\fzl.txt'
		pattern = ur"(处方[一二三四五六七八九十]*)[:：；][ ]*([^处方]*)"
		self.__prescritionNamePattern__ = re.compile(pattern)
	
	def _get_prescriptions_(self, sourceText):
		items = filter(lambda(x):len(x) > 0, [item.strip() for item in sourceText.strip().split('\n')])
		
		filter1 = PrescriptionQuantityFilter1()
		quantity = 0
		unit = None
		name = None
		prescriptions = []
		currentPrescription = None
		for item in items:
			m = self.__prescritionNamePattern__.match(item)	
			if m:
				if currentPrescription:
					prescriptions.append(currentPrescription)
				currentPrescription = {}

				if m.group(1) != "处方":
					name = m.group(1)
				if len(m.group(2)) > 0:
					name = m.group(2)
				
				if name:
					currentPrescription['name'] = name
				continue
			
			if 'comment' in currentPrescription:
				currentPrescription['comment'] += "\n" + item
				continue
			
			if not 'components' in currentPrescription:
				quantity, unit, otherText = filter1.splitByQuantity(item)
				parser1 = ComponentsParser1([' '], SingleComponentParser1())
				components = parser1.getComponents(otherText)
				if len(components) > 0:
					currentPrescription['components'] = components
				if quantity > 0:
					currentPrescription['quantity'] = quantity
					currentPrescription['unit'] = unit
				continue
			if not 'quantity' in currentPrescription:
				quantity, unit, otherText = filter1.splitByQuantity(item)
				if quantity > 0:
					currentPrescription['quantity'] = quantity
					currentPrescription['unit'] = unit
				else:
					currentPrescription['comment'] = item
					
		if currentPrescription:
			prescriptions.append(currentPrescription)
		else:
			print "**" + sourceText
			
		emptyPrescription = {"name":"", "comment":"", "quantity":0, "unit":""}
		for prescription in prescriptions:
			Utility.apply_default_if_not_exist(prescription, emptyPrescription)
		return prescriptions
	
	def __exact_detail_situation__(self, sourceText, targetDictionary):
		diagnosis_keywords =[u'处方：', u'处方一：', u'处方: ', u'处方；']
		
		targetDictionary[u'diagnosis'] = ""
		index = -1
		for keyword in diagnosis_keywords:
			index = sourceText.find(keyword)
			if(index >= 0):
				targetDictionary[u'description'] = sourceText[:index]
				targetDictionary[u'diagnosis'] = sourceText[index:]
				break
		
		if (index < 0):
			targetDictionary[u'description'] = sourceText		
		
		targetDictionary['prescriptions'] = self._get_prescriptions_(targetDictionary['diagnosis'])
			
	def __exact_detail__(self, whichTime, sourceText):
		comment_keywords = (u'［辨证］', u'［按语］', u'［按语)')
		index = -1
		detail = {u'order': whichTime}
		for keyword in comment_keywords:
			temp_index = sourceText.find(keyword)
			if temp_index < 0:
				continue
			if index < 0 or temp_index < index:
				index = temp_index
			
		if(index >= 0):
			self.__exact_detail_situation__(sourceText[:index], detail)
			detail[u'comments'] = sourceText[index:]				
			return detail
			
		self.__exact_detail_situation__(sourceText, detail)		
		return detail
		
	def _create_all_details__(self, which_time, sourceText, targetDetails):
		index = sourceText.find(u'诊］', 3)
		if (index > 0):
			detailItem = self.__exact_detail__(which_time, sourceText[:index - 2].strip())		
			targetDetails.append(detailItem)
			self._create_all_details__(which_time + 1, sourceText[index - 2:].strip(), targetDetails)
		else:
			detailItem = self.__exact_detail__(which_time, sourceText)			
			targetDetails.append(detailItem)
	
	def __create_consilia__(self, title, content):
		content = content[content.index(title) + len(title):].strip()
		keywords = (u'［初诊］', u'［一诊］', u'［诊治］')
		
		consilia = {}
		details = []
		description = ""
		for keyword in keywords:
			index = content.find(keyword)
			if(index >= 0):
				description = content[:index]
				content = content[index:]			
				break

		self._create_all_details__(1, content.strip(), details)
		Utility.apply_default_if_not_exist( details[0], {"description" : ""})
		details[0]['description'] = description + details[0]['description']
		consilia[u'details'] = details
		return consilia
	
	def _exact_title_information__(self, sourceText):
		titleInfo = {}
		items = []
		index = sourceText.find(u'(')
		if (index < 0):
			items.append(sourceText.strip())
		else:
			toIndex = len(sourceText) - 1
			items.extend([item.strip() for item in sourceText[index+1:toIndex].split(u'、')])
			items.append(sourceText[0:index].strip())
			
		titleInfo[u'diseaseNames'] = filter(lambda(x):len(x) > 0, items)
		return titleInfo
		
	def getAll(self):			
		sourceFile = codecs.open(self._source_file_fullpath, 'r', 'utf-8', 'ignore')
		content = sourceFile.read()
		sourceFile.close()
		
		content = content.replace("1O", "10")
		sourceFileWriter = codecs.open(self._source_file_fullpath, 'w', 'utf-8')
		sourceFileWriter.write(content)
		sourceFileWriter.close()
	
		items = []
		matches = re.findall(ur"(\d{1,2}\u3001.+)", content, re.M)
		for i in range(len(matches)):
			startContent = matches[i]
			if i == len(matches) - 1:
				'''last sourceText'''
				sourceText = content[content.index(startContent):]
			else:
				sourceText = content[content.index(startContent):content.index(matches[i+1])]
			sourceText = sourceText.strip()
			index = startContent.find(u'、') + 1
			titileText = startContent[index:].strip()

			consilia = {'comeFrom':{'bookTitle': u'范中林六经辨证医案'}, u'author':u'范中林'}
			titleDetail = self._exact_title_information__(titileText)	
			Utility.update_dict(consilia, titleDetail)	
			Utility.update_dict(consilia, self.__create_consilia__(titileText, sourceText))
			items.append(consilia)
			
		return items

if __name__ == "__main__":
	provider = Provider_fzl()
	items = provider.getAll()
	
	to_file = os.path.dirname(__file__) + '\\fzl_converted.txt'
	file_writer = codecs.open(to_file, 'w', 'utf-8', 'ignore')
	

	detailDefault = {u'description' : "None", u'comment' : "None", "diagnosis" : "None", "comments" : "None"}
	for item in items:
		for detail in item['details']:
			Utility.apply_default_if_not_exist(detail, detailDefault)
# 			file_writer.write("index:" + str(detail[u'order']) + "\n")
# 			file_writer.write("description:" + detail[u'description'] + "\n")
# 			file_writer.write("diagnosis:" + detail[u'diagnosis'] + "\n")
#  			file_writer.write("comments:" + detail[u'comments'] + "\n")

# 			file_writer.write(detail[u'description'] + "\n")
# 			file_writer.write("\n")
# 			file_writer.write(detail[u'diagnosis'] + "\n")
# 			file_writer.write("\n")
# 			file_writer.write(detail[u'comments'] + "\n")
# 			file_writer.write("\n")
			for prescription in detail['prescriptions']:
				file_writer.write(prescription["name"] + "\n")
				#if 'components' in prescription:
				for component in prescription['components']:
					file_writer.write(Utility.convert_dict_to_string(component)+ "\n") 
				file_writer.write(str(prescription["quantity"]) + " " + prescription["unit"] + "\n")
				file_writer.write(prescription["comment"] + "\n")
	file_writer.close()
	print "done"
