# -*- coding: utf-8 -*-
import json
from tqdm import tqdm

source = '../JSON/test_data.json'
output = 'ChunkJSON/'
chunk_size = 15

def dictToJson(chunk_number, data):
    '''
    将data另存为test_data_${chunk_number}.json
    :param chunk_number:
    :param data:
    :return:
    '''
    with open(output + "test_data_" + str(chunk_number) + '.json', 'w', encoding="GBK") as f:
        f.write(json.dumps(data, indent=4))

def jsonToChunk(filename = source):
    with open(filename, 'r', encoding='utf-8') as f:
        res = f.read()
        data = json.loads(res)
        user_ids = list(data.keys())
        temp = {}
        chunk_number = 1
        for x in tqdm(range(len(user_ids))):
            temp[user_ids[x]] = data[user_ids[x]]
            if((x + 1) % chunk_size == 0 ):
                dictToJson(chunk_number, temp)
                temp.clear()
                chunk_number += 1
        if(len(temp.keys()) != 0):
            dictToJson(chunk_number, temp)
            temp.clear()

if __name__ == '__main__':
    jsonToChunk()
    # TODO 按照题目来分块