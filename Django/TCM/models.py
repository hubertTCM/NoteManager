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

class Disease(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField(null=True)

class YiAnDetail(models.Model):
    order = models.IntegerField()
    yiAnId = models.IntegerField()
    description = models.TextField(null = True)
    comments = models.TextField(null = True) 
    comeFrom = models.ForeignKey(DataSource, null = True)
    class Meta:
        unique_together = ['yiAnId', 'order'] # it is better to set primary key, however, it is not supported in django 1.4
    
class YiAnDiseaseConnection(models.Model):
    yiAn = models.ForeignKey(YiAnDetail)
    disease = models.ForeignKey(Disease)
    class Meta:
        unique_together = ['yiAn', 'disease'] # it is better to set primary key, however, it is not supported in django 1.4
    
class YiAnOwner(models.Model):
    yiAn = models.ForeignKey(YiAnDetail)
    author = models.ForeignKey(Person)
    class Meta:
        unique_together = ['yiAn', 'author'] 

#处方： 麻黄10克 甘草30克 葱白60克 二剂
class YiAnPrescription(models.Model): 
    yiAnDetail = models.ForeignKey(YiAnDetail, null = False)
    name = models.CharField(max_length=300, null = True) #like 处方一
    allHerbText = models.CharField(max_length=300, null = False) #used for search    
    unit = models.CharField(max_length=255, null = True)
    quantity = models.FloatField(null=True) #like 二付
    comment = models.TextField(null=True)
    
class YiAnComposition(models.Model):
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
    
class TreatmentMethod(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

class Clause(models.Model): 
    comeFrom = models.ForeignKey(DataSource, null = False)
    index = models.IntegerField(null = False)
    content = models.TextField(null = False)
    
class BookSection(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self')
    class Meta:
        unique_together = ['name', 'parent']
    
class ClauseSection(models.Model):
    clause = models.ForeignKey(Clause)
    section = models.ForeignKey(BookSection)
    class Meta:
        unique_together = ['section', 'clause']
    
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
    allHerbText = models.CharField(max_length=300, null = False) #used for search
    comeFrom = models.ForeignKey(DataSource, null=True)
    comment = models.TextField(null=True)
    
#Prescription may composite with prescription and herb. For example: 茵陈五苓散
class PrescriptionComposition(models.Model):
    prescription = models.ForeignKey(Prescription, null=False)
    component = models.CharField(max_length=255, null=False)
    unit = models.ForeignKey(HerbUnit, null=True)
    quantity = models.FloatField(null=True) 
    comment = models.TextField(null=True)
    class Meta:
        unique_together = ['prescription', 'component']

class PrescriptionClauseConnection(models.Model):
    clause = models.ForeignKey(Clause)
    prescription = models.ForeignKey(Prescription)
    class Meta:
        unique_together = ['clause', 'prescription']
        
class PrescriptionTreatmentMethod(models.Model):
    method = models.ForeignKey(TreatmentMethod)
    prescription = models.ForeignKey(Prescription)
    class Meta:
        unique_together = ['method', 'prescription']
        