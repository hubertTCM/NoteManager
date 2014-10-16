# -*- coding: utf-8 -*-
import os
import sys
import Utils.Utility
def append_ancestors_to_system_path(levels):
    parent = os.path.dirname(__file__)
    for i in range(levels):
        sys.path.append(parent)
        parent = os.path.abspath(os.path.join(parent, ".."))

append_ancestors_to_system_path(2)

reload(sys)
os.environ.update({"DJANGO_SETTINGS_MODULE":"TCM.settings"})

from django.core.management import setup_environ
import TCM.settings
from TCM.models import *
setup_environ(TCM.settings)

class UnitImporter:
    def doImport(self, name):   
        if not name:
            return None
                
        unit, is_created = HerbUnit.objects.get_or_create(name = name) 
        if is_created:
            unit.save()
        return unit

class PersonImporter:
    def doImport(self, name):
        person, isCreated = Person.objects.get_or_create(name = name)
        if (isCreated):
            person.save()
            
        return person

class SourceImporter:
    def doImport(self, sourceInfo):
        bookTitle = Utils.Utility.Utility.get_value('bookTitle', sourceInfo)#sourceInfo['bookTitle']
        url = Utils.Utility.Utility.get_value('url', sourceInfo)#sourceInfo['url']
        source = None
        isCreated = False
        
        if (bookTitle and url):
            source, isCreated = DataSource.objects.get_or_create(bookTitle = bookTitle, url = url)
        else:
            if bookTitle:
                source, isCreated = DataSource.objects.get_or_create(bookTitle = bookTitle)
            if url:
                source, isCreated = DataSource.objects.get_or_create(url = url)
                
        if isCreated:
            source.save()
            
        return source
        