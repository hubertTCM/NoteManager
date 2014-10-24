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
        
        items = {ur"烂喉（疒丹）痧":ur"烂喉痧",ur"肺结棱":ur"肺结核", ur"自芍":ur"白芍",ur"焦兰仙":ur"焦三仙"}
        items.update({ur"疆蚕":ur"僵蚕", ur"值蚕":ur"僵蚕", ur"苏术":ur"苏木", ur"薏苡米":ur"薏苡仁", ur"葶苈于":ur"葶苈子"})
        items.update({ur"蝉表":ur"蝉衣", ur"生地愉":ur"地榆", ur"白芥于":ur"白芥子", ur"戚灵仙":ur"威灵仙"})
        items.update({ur"川檩子":ur"川楝子", ur"川楝于":ur"川楝子", ur"漩吴萸":ur"淡吴萸", ur"阿胶球":ur"阿胶珠", ur"术香":ur"木香"})
        items.update({ur"郁盒":ur"郁金", ur"片僵蚕":ur"片僵黄", ur"太黄":ur"大黄",ur"朴骨脂":ur"补骨脂"})
        items.update({ur"黄苓":ur"黄芩", ur"川樟子":ur"川楝子",ur"川草解":ur"川萆薢", ur"厚扑":ur"厚朴"})
        items.update({ur"粉月皮":ur"粉丹皮", ur"神血":ur"神曲", ur"阿腔":ur"阿胶", ur"瓜萎皮":ur"瓜蒌皮"})
        items.update({ur"千姜":ur"干姜", ur"五睐子":ur"五味子", ur"复盆子":ur"覆盆子"})
        items.update({ur"1O":ur"10", ur"4 5克":ur"45克", ur"I克":ur"1克"})
        items.update({ur"1 5克":ur"15克", ur"1 8克":ur"18克", ur"O 6克":ur"0.6克",ur"z0克":ur"20克" })
        items.update({ur"克分冲":ur"克(分冲)"})
        #content = content.replace("1O", "10")
        for key in items:
            content = content.replace(key, items[key])
        sourceFileWriter = codecs.open(filePath + "-updated", 'w', 'utf-8')
        sourceFileWriter.write(content)
        sourceFileWriter.close()
        

if __name__ == "__main__":
    print "done"
