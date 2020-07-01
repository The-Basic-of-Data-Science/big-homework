# -*- coding: utf-8 -*-
import json
import urllib
import zipfile
import os
from tqdm import tqdm
source = '../JSON/sample.json'
source_all = '../JSON/test_data.json'
python_output = 'Python/'

def retriveOne(user_id, case_id, upload_id, url):
    '''
    拉取Url的Zip中用户提交的Python文件
    :param url: oss远端的ZIP地址
    :return: void
    '''
    temp = python_output + 'temp.zip'
    urllib.request.urlretrieve(url, temp)
    with zipfile.ZipFile(temp, 'r') as zzz:
        f_name = zzz.namelist()[0]
        zzz.extractall(path = python_output)
        with zipfile.ZipFile(python_output + f_name, 'r') as f:
            f.extract('main.py', python_output)
            name = python_output + str(user_id) + "/" + str(case_id) + "/" + str(upload_id) + "_" + f_name.split('.')[0] + '.py'
            try:
                os.rename(python_output + 'main.py', name)
            except Exception as e:
                str(e)
        os.remove(python_output + f_name) # 删除临时的文件
    os.remove(python_output + 'temp.zip') # 删除临时的压缩包

def retriveAllUploads(filename = source):
    '''
    拉取指定json文件中的所有的Python文件
    :param filename:json文件
    :return: void
    '''
    user_number = 0
    with open(filename, 'r', encoding='utf-8') as f:
        res = f.read()
        data = json.loads(res)
        for user_id in data.keys():
            user_number += 1
            print("UserNumber:{}".format(user_number))
            cases = data[user_id]['cases']
            # 处理每一个Case
            for case in tqdm(cases):
                case_id = case['case_id']
                uploads = case['upload_records']
                # 如果没有这个目录则新建
                if(not os.path.exists(python_output + str(user_id) + "/" + str(case_id) + "/")):
                    os.makedirs(python_output + str(user_id) + "/" + str(case_id) + "/")
                for upload in uploads:
                    upload_id = upload['upload_id']
                    retriveOne(user_id, case_id, upload_id, upload['code_url'])

if __name__ == '__main__':
    retriveAllUploads()