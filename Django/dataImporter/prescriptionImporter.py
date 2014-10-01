# -*- coding: utf-8 -*-
import os
import sys

from dataImporter.Utils.Utility import *
from dataImporter.Utils.HerbUtil import HerbUtility
from DataSourceImporter import *

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

class SinglePrescriptionImporter:
    def __init__(self, prescription, herbUtility):
        self._prescription = prescription
        self._source_importer = SourceImporter()
        self._herb_utility = herbUtility
        
        self._allHerbText = ""

        for component in self._prescription['components']:
            herbName = self._herb_utility.get_herb_name(component['medical'])
            component['medical'] = herbName
            self._allHerbText += herbName + " "
            
        self._allHerbText = self._allHerbText.strip()
        
    def __is_imported__(self):
        return False

    def __get_unit__(self, name):   
        if not name:
            return None
                
        unit, is_created = HerbUnit.objects.get_or_create(name = name) 
        if is_created:
            unit.save()
        return unit
    
    def __get_prescription__(self, name):
        prescription, is_created = Prescription.objects.get_or_create(name = name)
        if is_created:
            prescription.comeFrom = Utility.run_action_when_key_exists(u'comeFrom', self._prescription, self._source_importer.import_source)
            prescription.save()
        return prescription
           
  
    def __import_composition__(self, db_prescription, component):
        try:
            db_composition = PrescriptionComponent()
            db_composition.component = component['medical']
            db_composition.prescription = db_prescription
            db_composition.quantity = component['quantity']
            db_composition.unit = self.__get_unit__(component['unit'])
            db_composition.comment = component['comments']
            db_composition.save()

        except Exception,ex:
            print Exception,":",ex, "prescription: ",db_prescription.name, " medical: ",component['medical'], " quantity", component['quantity'], " unit", component['unit']
    
    def do_import(self):
        try:
            if self.__is_imported__():
                return

            db_prescription = Prescription()
            db_prescription.category = 'Prescription'  
            db_prescription.comeFrom = Utility.run_action_when_key_exists(u'comeFrom', self._prescription, self._source_importer.import_source)
            db_prescription.comment = self._prescription['comment']
            db_prescription.allHerbText = self._allHerbText
            db_prescription.save()

            for component in self._prescription['components']:
                self.__import_composition__(db_prescription, component)

            return db_prescription
        except Exception,ex:
                print Exception,":",ex
                return None

herbUtility = HerbUtility()

class PrescriptionsImporter:
    def __init__(self, prescriptions):
        self._prescriptions = prescriptions
    
    def do_import(self):
        db_prescriptions = []
        for prescription in self._prescriptions:
            try:
                importer = SinglePrescriptionImporter(prescription, herbUtility)
                item = importer.do_import()
                if item:
                    db_prescriptions.append(item)
            except Exception,ex:
                    print Exception,":",ex
        return db_prescriptions
            
if __name__ == "__main__":
    print "no data to import"