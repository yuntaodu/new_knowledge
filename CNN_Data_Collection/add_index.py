import json
from collections import OrderedDict

# 加载原始 JSON 文件
with open('/home/jiangkailin/project/New_Knowledge/entity_json/EUQA_mini_2_4o.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 创建一个新的列表，用于存储添加了 id 字段的数据
new_data = []

# 为每条数据添加递增的 id 字段，并确保 id 在最前面
for idx, item in enumerate(data, start=1):
    ordered_item = OrderedDict()
    ordered_item['id'] = idx  # 将 id 放在最前面
    ordered_item.update(item)  # 添加其他字段
    new_data.append(ordered_item)

# 将更新后的数据保存到新的 JSON 文件
with open('/home/jiangkailin/project/New_Knowledge/entity_json/EUQA_mini_2_4o_index.json', 'w', encoding='utf-8') as file:
    json.dump(new_data, file, ensure_ascii=False, indent=4)

print("已成功添加 id 字段，并确保其在每条数据的最前面，结果保存到 da_with_id.json 文件中")
