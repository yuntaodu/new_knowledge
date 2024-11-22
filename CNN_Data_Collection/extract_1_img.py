import json

# 读取原始JSON文件
input_file_path = '/home/jiangkailin/project/New_Knowledge/train_data/data/random_40_content.json'
output_file_path = '/home/jiangkailin/project/New_Knowledge/train_data/data/random_40_content_1_img.json'

with open(input_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 遍历数据并添加新字段
for item in data:
    # 检查 images 和 descriptions 字段是否存在
    images = item.get('images', [])
    descriptions = item.get('descriptions', [])

    if len(images) == 1:
        # 如果 images 数量等于 1
        item['train_img_url'] = images[0]
        item['train_img_caption'] = descriptions[0] if descriptions else ''
    elif len(images) > 1:
        # 如果 images 数量大于 1
        item['train_img_url'] = images[0]
        item['train_img_caption'] = descriptions[0] if descriptions else ''

# 将处理后的数据写入新的JSON文件
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

print("数据处理完成，已生成新的JSON文件。")
