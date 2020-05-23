# -*- coding: utf-8 -*-

'''
统计数据，根据之前筛选出来的有效性
1. 我们使用OurModel/AfterData/filename.json中数据再次之前我们3部分的运算,写入到CsvResult下的 分数统计.csv文件夹下
   表格表头:case_id,平均分，中位数，众数，尝试人数，做对人数，平均提交次数，用例总数
2. 我们使用OurModel/AfterData/filename.json中数据再次之前我们3部分的运算,写入到CsvResult下的 用户行为统计.csv文件夹下
   表格表头:user_id,case_id,提交次数，每次分数(|分隔)，分数变化
3. 我们使用OurModel/AfterData/filename.json中数据统计尝试和完成人数写入到CsvResult下的 尝试人数.csv
   表格表头:uid,case_id,尝试人数,做对人数
4. 补充统计内容:
   第一次有效提交分数,最终得分
'''