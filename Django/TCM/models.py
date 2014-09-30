# -*- coding: utf-8 -*-
import datetime
import os
import sys

from django.db import models
from django.db.models import Q

"""TCM = Traditional Chinese Medical"""
class Person(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
  
class DataSource(models.Model):
    bookTitle = models.CharField(max_length=255, null = True)
    url = models.URLField(null = True)

class HerbUnit(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(null=True)
    
class YiAnDetail(models.Model):
    order = models.IntegerField()
    yiAnId = models.IntegerField()
    
    description = models.TextField(null = True)

    comments = models.TextField(null = True) 
    
    class Meta:
        unique_together = ['yiAnId', 'order'] # it is better to set primary key, however, it is not supported in django 1.4
    
# class ConsiliaDiseaseConnection(models.Model):
    # consilia = models.ForeignKey(ConsiliaSummary)
    # disease = models.ForeignKey(Disease)
    # class Meta:
        # unique_together = ['consilia', 'disease']
 
#处方： 麻黄10克 甘草30克 葱白60克 二剂
class YiAnPrescription(models.Model): 
    YiAnDetail = models.ForeignKey(YiAnDetail, null = False)
    
    unit = models.CharField(max_length=255, null = True)
    quantity = models.FloatField(null=True)
    comment = models.TextField(null=True)
    
class YiAnComponent(models.Model):
    prescription = models.ForeignKey(YiAnPrescription, null = False)
    component = models.TextField(max_length=255, null=False)
    unit = models.ForeignKey(HerbUnit, null=True)
    quantity = models.FloatField(null=True) 
    comment = models.TextField(null=True)       
    
class MedicalNote(models.Model):  
    author = models.ForeignKey(Person)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True)
    creationTime = models.DateField(null = True)
    comeFrom = models.ForeignKey(DataSource, null = True)
    
    def json(self):
        json_object = {}
        json_object[u'id'] = self.id
        json_object[u'author'] = self.author.name
        json_object[u'title'] = self.title
        json_object[u'content'] = self.content
         
        if (self.creationTime != None):
            json_object[u'creationTime'] = str(self.creationTime)          
        if (self.comeFrom):
            json_object[u'source'] = self.comeFrom.category
            json_object[u'source_id'] = self.comeFrom.id
        return json_object
    
class ClauseCategory(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
        
class Clause(models.Model): 
    comeFrom = models.ForeignKey(DataSource, null = False)
    index = models.IntegerField(null = False)
    content = models.TextField(null = False)
    
class ClauseCategoryReference(models.Model):
    clause = models.ForeignKey(Clause) 
    category = models.ForeignKey(ClauseCategory)
    class Meta:
        unique_together = ['clause', 'category']
                  
class Herb(models.Model):
    name = models.CharField(max_length=255, null=False, primary_key=True)
    description = models.TextField(null=True)
    
class HerbAlias(models.Model):
    name = models.CharField(max_length=255, null=False, primary_key=True)
    standardName = models.ForeignKey(Herb, null=False)
    class Meta:
        unique_together = ['name', 'standardName']

        
class Prescription(models.Model): 
    name = models.CharField(max_length=255, null=False, primary_key=False)
    comeFrom = models.ForeignKey(DataSource, null=True)
    comment = models.TextField(null=True)
    
#Prescription may composite with prescription and herb. For example: 茵陈五苓散
class HerbComponent(models.Model):
    prescription = models.ForeignKey(Prescription, null=False)
    component = models.ForeignKey(Herb, null=False)
    unit = models.ForeignKey(HerbUnit, null=True)
    quantity = models.FloatField(null=True) 
    comment = models.TextField(null=True)
    class Meta:
        unique_together = ['prescription', 'component']
        
class PrescriptionComponent(models.Model):
    prescription = models.ForeignKey(Prescription, related_name='prescription', null=False)
    component = models.ForeignKey(Prescription, null=False)
    unit = models.ForeignKey(HerbUnit, null=True)
    quantity = models.FloatField(null=True) 
    comment = models.TextField(null=True)
    class Meta:
        unique_together = ['prescription', 'component']
        