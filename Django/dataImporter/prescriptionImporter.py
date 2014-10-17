# -*- coding: utf-8 -*-
import os
import sys

from dataImporter.Utils.Utility import *
from dataImporter.Utils.HerbUtil import HerbUtility
from DataSourceImporter import *
from thirdParty.cnsort import cnsort

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
    def __init__(self, herbUtility):
        self.__sourceImporter__ = SourceImporter()
        self._herb_utility = herbUtility
        
        
    def __is_imported__(self):
        return False

    def __getUnit__(self, name):   
        if not name:
            return None
                
        unit, is_created = HerbUnit.objects.get_or_create(name = name) 
        if is_created:
            unit.save()
        return unit
  
    def __importComposition__(self, db_prescription, component):
        try:
            db_composition = PrescriptionComposition()
            db_composition.component = component['medical']
            db_composition.prescription = db_prescription
            db_composition.quantity = component['quantity']
            db_composition.unit = self.__getUnit__(component['unit'])
            db_composition.comment = component['comments']
            db_composition.save()

        except Exception,ex:
            print Exception,":",ex, "prescription: ",db_prescription.name, " medical: ",component['medical'], " quantity", component['quantity'], " unit", component['unit']
    
    def doImport(self, source):
        try:
            if self.__is_imported__():
                return
            
            names = []
            for item in source['components']: 
                #keep original name in prescription, 
                #ensure there is no error by conversion
                herbs = self.__herbUtility__.extractHerbsFromAbbreviation(item['medical'])
                for herb in herbs:
                    names.append(herb)
            cnsort.cnsort(names)

            db_prescription = Prescription()
            db_prescription.name = source['name']
            db_prescription.comeFrom = Utility.run_action_when_key_exists(u'comeFrom', source, self.__sourceImporter__.doImport)
            db_prescription.comment = source['comment']
            db_prescription.allHerbText = " ".join(names)
            db_prescription.save()

            for component in self._prescription['components']:
                self.__importComposition__(db_prescription, component)

            return db_prescription
        except Exception,ex:
                print Exception,":",ex
                return None

herbUtility = HerbUtility()

class PrescriptionsImporter:
    def __init__(self, prescriptions):
        self._prescriptions = prescriptions
    
    def doImport(self):
        db_prescriptions = []
        for prescription in self._prescriptions:
            try:
                importer = SinglePrescriptionImporter(prescription, herbUtility)
                item = importer.doImport()
                if item:
                    db_prescriptions.append(item)
            except Exception,ex:
                    print Exception,":",ex
        return db_prescriptions
            
if __name__ == "__main__":
    print "no data to import"