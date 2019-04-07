# coding=utf-8
# 获取输入数据
import sys
import json
input_file = sys.argv[1]
lines = open(input_file, "r").readlines()
lines = [line.strip() for line in lines]

# 获取键值
keys = lines[0].split(',')

line_num = 1
total_lines = len(lines)

parsed_datas = []
while line_num < total_lines:
        values = lines[line_num].split(",")
        parsed_datas.append(dict(zip(keys, values)))

        line_num = line_num + 1

json_str = json.dumps(parsed_datas, ensure_ascii=False, indent=4)
output_file = input_file.replace("csv", "json")

# write to the file
f = open(output_file, "w")
f.write(json_str)
f.close()

print("解析结束！")
