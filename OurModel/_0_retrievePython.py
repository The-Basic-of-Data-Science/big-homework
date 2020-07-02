# -*- coding: utf-8 -*-
import json
import urllib
import zipfile
import os
from tqdm import tqdm

source_all = '../JSON/test_data.json'


class RetrieveClass:
    def __init__(self, name, source, output):
        self.name = name
        # 源文件目录
        self.source = source
        # 输出文件目录
        self.output = output

    def retrieve_upload(self, user_id, case_id, upload_id, url):
        '''
        拉取Url的Zip中用户提交的Python文件
        :param user_id 拉取的用户的id
        :param case_id 拉取的题目的id
        :param upload_id 上传的id
        :param url: oss远端的ZIP地址
        :return: void
        '''
        temp = self.output + 'temp.zip'
        urllib.request.urlretrieve(url, temp)
        with zipfile.ZipFile(temp, 'r') as zzz:
            f_name = zzz.namelist()[0]
            zzz.extractall(path=self.output)
            with zipfile.ZipFile(self.output + f_name, 'r') as f:
                f.extract('main.py', self.output)
                name = self.output + str(user_id) + "/" + str(case_id) + "/" + str(upload_id) + "_" + f_name.split('.')[
                    0] + '.py'
                try:
                    os.rename(self.output + 'main.py', name)
                except Exception as e:
                    str(e)
            os.remove(self.output + f_name)  # 删除临时的文件
        os.remove(self.output + 'temp.zip')  # 删除临时的压缩包

    def retrieve_uploads(self):
        '''
        拉取指定json文件中的所有的Python文件
        :param source:json文件
        :param output:python文件的下载到哪
        :return: void
        '''
        user_number = 0
        with open(self.source, 'r', encoding='utf-8') as f:
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
                    if (not os.path.exists(self.output + str(user_id) + "/" + str(case_id) + "/")):
                        os.makedirs(self.output + str(user_id) + "/" + str(case_id) + "/")
                    for upload in uploads:
                        upload_id = upload['upload_id']
                        self.retrieve_upload(user_id, case_id, upload_id, upload['code_url'])


if __name__ == '__main__':
    temp = RetrieveClass("temp", '../JSON/sample.json', './Python/')
    temp.retrieve_uploads()
