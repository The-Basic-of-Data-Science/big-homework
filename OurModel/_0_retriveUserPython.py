# -*- coding: utf-8 -*-
import json
import urllib
import zipfile
import os
from tqdm import tqdm

source_all = '../JSON/test_data.json'
'Python/'

def retriveOne(user_id, case_id, upload_id, url, output):
    '''
    拉取Url的Zip中用户提交的Python文件
    :param url: oss远端的ZIP地址
    :return: void
    '''
    temp = output + 'temp.zip'
    urllib.request.urlretrieve(url, temp)
    with zipfile.ZipFile(temp, 'r') as zzz:
        f_name = zzz.namelist()[0]
        zzz.extractall(path = output)
        with zipfile.ZipFile(output + f_name, 'r') as f:
            f.extract('main.py', output)
            name = output + str(user_id) + "/" + str(case_id) + "/" + str(upload_id) + "_" + f_name.split('.')[0] + '.py'
            try:
                os.rename(output + 'main.py', name)
            except Exception as e:
                str(e)
        os.remove(output + f_name) # 删除临时的文件
    os.remove(output + 'temp.zip') # 删除临时的压缩包

def retriveAllUploads(source, output):
    '''
    拉取指定json文件中的所有的Python文件
    :param source:json文件
    :return: void
    '''
    user_number = 0
    with open(source, 'r', encoding='utf-8') as f:
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
                if(not os.path.exists(output + str(user_id) + "/" + str(case_id) + "/")):
                    os.makedirs(output + str(user_id) + "/" + str(case_id) + "/")
                for upload in uploads:
                    upload_id = upload['upload_id']
                    retriveOne(user_id, case_id, upload_id, upload['code_url'], output)

if __name__ == '__main__':
    retriveAllUploads('../JSON/sample.json', './Python/')