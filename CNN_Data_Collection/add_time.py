import json
import os
import random

# 读取 JSON 文件
input_file = '/home/jiangkailin/project/New_Knowledge/entity_json/summary_test_content.json'
output_file = '/home/jiangkailin/project/New_Knowledge/entity_json/summary_test_content_add_time.json'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 遍历数据并生成新的 time 字段
for item in data:
    if 'timestamp' in item and len(item['timestamp']) >= 4:
        # 获取月份日期部分和年份
        full_date = item['timestamp'][2]  # e.g., "Wed April 10"
        year = item['timestamp'][3]
        
        # 提取需要的部分，即 "April 10"
        month_day = " ".join(full_date.split()[1:])  # "April 10"
        
        # 将月份日期和年份组合为新的格式
        formatted_date = f"{month_day}, {year}"
        
        # 在 item 中新增字段 time
        item['time'] = formatted_date

# 模板句子列表
templates = [
    "The news was reported on {time}.",
    "On {time}, the news was published.",
    "This news report was released on {time}.",
    "The report on this news came out on {time}.",
    "On {time}, the news coverage was made public.",
    "The report date for this news is {time}.",
    "This piece of news was announced on {time}.",
    "The news was officially reported on {time}."
]

# 遍历数据并更新 summary 字段
for item in data:
    if 'time' in item and 'Summary' in item:
        # 从模板中随机选择一个句子并替换 {time}
        intro_text = random.choice(templates).format(time=item['time'])
        
        # 将生成的句子添加到 summary 内容前面
        item['Summary'] = intro_text + " " + item['Summary']

# 将更新后的数据写回新的 JSON 文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("新字段 'time' 添加完成，并已更新 JSON 文件，添加模板文本到 Summary 字段。")



# import json
# import random

# # 模板句子列表
# templates = [
#     "The news was reported on {time}.",
#     "On {time}, the news was published.",
#     "This news report was released on {time}.",
#     "The report on this news came out on {time}.",
#     "On {time}, the news coverage was made public.",
#     "The report date for this news is {time}.",
#     "This piece of news was announced on {time}.",
#     "The news was officially reported on {time}."
# ]

# # 读取 JSON 文件
# input_file = '/home/jiangkailin/project/New_Knowledge/summary_test_content_time.json'
# output_file = '/home/jiangkailin/project/New_Knowledge/summary_test_content_add_time.json'

# with open(input_file, 'r', encoding='utf-8') as f:
#     data = json.load(f)

# # 遍历数据并更新 summary 字段
# for item in data:
#     if 'time' in item and 'summary' in item:
#         # 从模板中随机选择一个句子并替换 {time}
#         intro_text = random.choice(templates).format(time=item['time'])
        
#         # 将生成的句子添加到 summary 内容前面
#         item['summary'] = intro_text + " " + item['summary']

# # 将更新后的数据写回新的 JSON 文件
# with open(output_file, 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

# print("已更新 JSON 文件，并添加模板文本到 summary 字段。")
