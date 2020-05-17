# -*- coding: utf-8 -*-
import csv

def printDict(targetDict,keys):
    print(keys[0],targetDict[keys[0]])
    print(keys[-1],targetDict[keys[-1]])
    # for key in keys:
    #     print(key,targetDict[key])

def writeCSV(fileName,temp):
    # 向外写temp
    with open(fileName,"a+",encoding="utf-8",newline = "") as f:
        writer = csv.writer(f)
        writer.writerow(temp)