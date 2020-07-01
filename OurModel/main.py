# -*- coding: utf-8 -*-
from OurModel import _0_retriveUserPython
from OurModel import _1_findValid
from OurModel import _2_Statics

if __name__ == '__main__':
    source = '../JSON/sample.json'
    python_source = './Python/'
    valid_csv_output = './CsvResult'
    # _0_retriveUserPython.retriveAllUploads(source, python_source)
    _1_findValid.findValid(python_source, source, valid_csv_output)
    _2_Statics.my_statistics()