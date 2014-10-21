# -*- coding: utf-8 -*-
import sys
import os
import codecs
import re

class Updater:
    def update(self, filePath):
        sourceFileReader = codecs.open(filePath, 'r', 'utf-8', 'ignore')
        content = sourceFileReader.read()
        sourceFileReader.close()
        
        items = {ur"烂喉（疒丹）痧":ur"烂喉痧", ur"赤自芍":ur"赤白芍",ur"焦兰仙":ur"焦三仙"}
        items.update({ur"1O":ur"10", ur"4 5克":ur"45克"})
        items.update({ur"1 5克":ur"15克", ur"1 8克":ur"18克", ur"O 6克":ur"0.6克" })
        items.update({ur"克分冲":ur"克(分冲)"})
        #content = content.replace("1O", "10")
        for key in items:
            content = content.replace(key, items[key])
        sourceFileWriter = codecs.open(filePath + "-updated", 'w', 'utf-8')
        sourceFileWriter.write(content)
        sourceFileWriter.close()
        

if __name__ == "__main__":
    print "done"
