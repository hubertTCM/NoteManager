# -*- coding: utf-8 -*-
import os
import sys
from django.core.management import setup_environ

from ConsiliaProvider.provider_fzl import *
from ConsiliaProvider.zmt import *
from dataImporter.Utils.Utility import *
from dataImporter.Utils.HerbUtil import HerbUtility

from thirdParty.cnsort import cnsort

def append_ancestors_to_system_path(levels):
    parent = os.path.dirname(__file__)
    for i in range(levels):
        sys.path.append(parent)
        parent = os.path.abspath(os.path.join(parent, ".."))

append_ancestors_to_system_path(2)

reload(sys)
os.environ.update({"DJANGO_SETTINGS_MODULE":"TCM.settings"})

from DataSourceImporter import *

from TCM.models import *
import TCM.settings
setup_environ(TCM.settings)


to_file = os.path.dirname(__file__) + '\\debug.txt'
file_writer = codecs.open(to_file, 'w', 'utf-8', 'ignore')

class YiAnPrescriptionImporter:
    def __init__(self):
        self.__unitImporter__ = UnitImporter()
        self.__herbUtility__ = HerbUtility()
    
    def __getQuantity__(self, source):
        if source > 0:
            return source
        return None
        
    def __importComponent__(self, source, prescription):
        composition = YiAnComposition()
        composition.prescription = prescription
        composition.component = source['medical']
        composition.quantity = self.__getQuantity__(source['quantity'])
        composition.unit = self.__unitImporter__.doImport(source['unit'])
        composition.comment = source['comments']
        composition.save()
        return composition
    def doImport(self, source, yiAnDetail):
        emptyPrescription = {"name":"", "comments":"", "quantity":0, "unit":""}
        Utility.apply_default_if_not_exist(source, emptyPrescription)
        
        compositions = []
        names = []
        for item in source['components']:
            herbs = self.__herbUtility__.extractHerbsFromAbbreviation(item['medical'])
            for herb in herbs:
                temp = item.copy()
                temp['medical'] = herb
                compositions.append(temp)
                names.append(herb)
        cnsort.cnsort(names)
        
        
        yiAnPrescription = YiAnPrescription()
        yiAnPrescription.yiAnDetail = yiAnDetail
        yiAnPrescription.name = source["name"]
        
        yiAnPrescription.allHerbText = " ".join(names)
        
        yiAnPrescription.quantity = self.__getQuantity__(source['quantity'])
        yiAnPrescription.unit = source['unit']
        
        yiAnPrescription.save()
        
        for component in compositions:
            self.__importComponent__(component, yiAnPrescription)
        return yiAnPrescription
class SingleImporter:
    def __init__(self):
        self.__sourceImporter__ = SourceImporter()
        self.__prescriptionImporter__ = YiAnPrescriptionImporter()
        self.__yiAnId__ = 1
            
    def __getSource__(self, sourceInfo):
        if not sourceInfo:
            return None
        return self.__sourceImporter__.doImport(sourceInfo)
    
    def __importAuthor__(self, authorName, yiAnDetail):
        if not authorName:
            return
        
        author, isCreated = Person.objects.get_or_create(name = authorName)
        if (isCreated):
            author.save()
            
        owner = YiAnOwner()
        owner.yiAn = yiAnDetail
        owner.author = author
        owner.save()

    def __importDiseas__(self, diseasNames, yiAnDetail):
        for diseasName in diseasNames:
            disease, isCreated = Disease.objects.get_or_create(name = diseasName)
            if (isCreated):
                disease.save() 
            diseaseConnection = YiAnDiseaseConnection()
            diseaseConnection.yiAn = yiAnDetail
            diseaseConnection.disease = disease
            diseaseConnection.save()
                
    def __importDetail__(self, source):
        file_writer.write("yiAnId:" + str(self.__yiAnId__) + "  order: " + str(source[u'order']) + " description:" + source[u'description'] + "\n")
        detail = YiAnDetail()
        detail.yiAnId = self.__yiAnId__
        detail.order = source[u'order']
        detail.description = source[u'description']
        detail.comments = source[u'comments']
        detail.comeFrom = self.__getSource__(self.__consiliaInfo__[u'comeFrom'])
        detail.save()
        
        for prescription in source['prescriptions']:
            self.__prescriptionImporter__.doImport(prescription, detail)
        
        return detail
        
    def __importYiAn__(self):
        detailDefault = {u'description' : None, u'comments' : None, 'prescriptions' : []}
        firstItem = None
        for sourceDetail in self.__consiliaInfo__[u'details']:
            Utility.apply_default_if_not_exist(sourceDetail, detailDefault)
            detail = self.__importDetail__(sourceDetail)
            if not firstItem:
                firstItem = detail
        
        self.__importDiseas__(self.__consiliaInfo__['diseaseNames'], firstItem)
        self.__importAuthor__(self.__consiliaInfo__['author'], firstItem)
        
        self.__yiAnId__ += 1    
                   
    def doImport(self, consilia): 
        self.__consiliaInfo__ = consilia 
        defaultInfo = { u'description' : None, u'comeFrom': None, u'author':None, u'diseaseNames':[]}
        Utility.apply_default_if_not_exist(self.__consiliaInfo__, defaultInfo) 
        self.__importYiAn__()

class Importer:  
    def __init__(self):
        self._consiliaSources = []
        self._consiliaSources.append(Provider_fzl())
        #self._consiliaSources.append(Provider_zmt())  
        
    def doImport(self):
        impoter = SingleImporter()
        for provider in self._consiliaSources:
            for consilia in provider.get_all_consilias():
                try:
                    impoter.doImport(consilia)             
                except Exception,ex:
                    print "***" + str(consilia)
                    print Exception,":",ex
                    file_writer.write(str(ex) + "\n")
                    
if __name__ == "__main__":
    importerInstance = Importer()
    importerInstance.doImport()
    print 'done'