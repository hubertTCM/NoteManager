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
	
	def __exact_detail_situation__(self, sourceText, targetDictionary):
		diagnosis_keywords =[u'处方：', u'处方一：', u'处方: ', u'处方；']
		index = -1
		for keyword in diagnosis_keywords:
			index = sourceText.find(keyword)
			if(index >= 0):
				targetDictionary[u'description'] = sourceText[:index]
				targetDictionary[u'diagnosis'] = sourceText[index:]
				#print 'description:  ' + targetDictionary['description']
				#print 'diagnosis:  ' + targetDictionary['diagnosis']
				break
		
		if (index < 0):
			targetDictionary[u'diagnosis'] = sourceText		
		
		targetDictionary['prescriptions'] = self._get_prescriptions_(targetDictionary['diagnosis'])
			#print 'diagnosis:  ' + targetDictionary['diagnosis']
			
	def __exact_detail__(self, whichTime, sourceText):
		comment_keywords = (u'［辨证］', u'［按语］', u'［按语)')
		index = -1
		detail = {u'index': whichTime}
		for keyword in comment_keywords:
			temp_index = sourceText.find(keyword)
			if temp_index < 0:
				continue
			if index < 0 or temp_index < index:
				index = temp_index
			
		if(index >= 0):
			self.__exact_detail_situation__(sourceText[:index], detail)
			detail[u'comments'] = sourceText[index:]
			#print 'comment:  ' + detail['comments']				
			return detail
			
		self.__exact_detail_situation__(sourceText, detail)		
		return detail
		
	def _create_all_details__(self, which_time, sourceText, targetDetails):
		index = sourceText.find(u'诊］', 3)
# 		keywords = (u'［初诊］', u'［一诊］', u'［诊治］')
# 		for keyword in keywords:
# 			index = sourceText.find(keyword)
# 			if(index >= 0):
# 				break
#  				consilia[u'description'] = content[:index]
#  				content = content[index:]
# 				print 'description:  ' + consilia['description'] 				
#  				break
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
# 				consilia[u'description'] = content[:index]
				description = content[:index]
				content = content[index:]
				#print 'description:  ' + consilia['description'] 				
				break

		self._create_all_details__(1, content.strip(), details)
		Utility.apply_default_if_not_exist( details[0], {"description" : ""})
		details[0]['description'] = description + details[0]['description']
		consilia[u'details'] = details
		return consilia
	
	def _exact_title_information__(self, sourceText):
		titleInfo = {}
		#print "** title: " + sourceText
		index = sourceText.find(u'(')
		if (index < 0):
			titleInfo[u'title'] = sourceText.strip()
		else:
			toIndex = len(sourceText) - 1
			titleInfo[u'title'] = sourceText[0:index].strip()
			titleInfo[u'diseaseName'] = [item.strip() for item in sourceText[index+1:toIndex].split(u'、')]
			#print "diseaseName: " +  " ## ".join(map(str, titleInfo['diseaseName']))			
		
		#print "** TCM: " + titleInfo['title'] 
		return titleInfo
	
	def _get_prescriptions_(self, sourceText):
		return []
	
	def get_all_consilias(self):			
		sourceFile = codecs.open(self._source_file_fullpath, 'r', 'utf-8', 'ignore')
		content = sourceFile.read()
		sourceFile.close()
	
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

			consilia = {u'bookTitle': u'范中林六经辨证医案'}
			titleDetail = self._exact_title_information__(titileText)	
			Utility.update_dict(consilia, titleDetail)	
			Utility.update_dict(consilia, self.__create_consilia__(titileText, sourceText))
			#yield consilia
			items.append(consilia)
			
		return items

if __name__ == "__main__":
	provider = Provider_fzl()
	items = provider.get_all_consilias()
	
	to_file = os.path.dirname(__file__) + '\\fzl_converted.txt'
	file_writer = codecs.open(to_file, 'w', 'utf-8', 'ignore')
	
	detailDefault = {u'description' : "None", u'comments' : "None", "diagnosis" : "None", "comments" : "None"}
	for item in items:
		for detail in item['details']:
			Utility.apply_default_if_not_exist(detail, detailDefault)
# 			file_writer.write("index:" + str(detail[u'index']) + "\n")
# 			file_writer.write("description:" + detail[u'description'] + "\n")
			file_writer.write("diagnosis:" + detail[u'diagnosis'] + "\n")
# 			file_writer.write("comments:" + detail[u'comments'] + "\n")
			file_writer.write("**\n")
	
	file_writer.close()
	print "done"
