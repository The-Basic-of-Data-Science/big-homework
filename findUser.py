# -*- coding: utf-8 -*-
import csv

'''
专门用来找8类题目都做了的
'''
with open("./OurModelOutPut/Result/all.csv", 'r', encoding="utf-8") as f:
    reader = csv.reader(f)
    for line in reader:
        if(line[0] == "用户编号"):
            continue
        if(len(eval(line[4])) == 8):
            print([line[0], len(eval(line[3]))])