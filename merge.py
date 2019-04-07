# coding=utf-8
# 获取输入数据
import glob
import time

csvx_list = glob.glob('*.csv')
print('总共发现%s个CSV文件'% len(csvx_list))
time.sleep(2) 
print('正在处理............')
for i in csvx_list:
    fr = open(i,'r').read()
    with open('csv_to_csv.csv','a') as f:
        f.write(fr)
    print('写入成功！')
print('写入完毕！')
print('10秒钟自动关闭程序！')
time.sleep(10)
# python pyinstaller.py -F 文件名
