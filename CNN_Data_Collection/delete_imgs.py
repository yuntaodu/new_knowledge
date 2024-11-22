import json
import os

# 原始 JSON 文件所在文件夹
input_folder = '/home/jiangkailin/project/New_Knowledge/clean_content'
# 输出 JSON 文件夹（用于存储过滤后的 JSON 文件）
output_folder = '/home/jiangkailin/project/New_Knowledge/clean_content_img'

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历 JSON 文件夹中的每个文件
for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        file_path = os.path.join(input_folder, filename)
        
        try:
            # 读取 JSON 文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 过滤数据，保留 images 字段数量在 1 到 5 之间的数据
            filtered_data = [item for item in data if 'images' in item and 1 <= len(item['images']) <= 5]
            
            # 修改输出文件名前缀
            new_filename = filename.replace("clean_content", "clean_content_img")
            output_file_path = os.path.join(output_folder, new_filename)
            
            # 将过滤后的数据写入新文件
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(filtered_data, f, ensure_ascii=False, indent=4)
            
            # 打印新 JSON 文件的数据数量
            print(f"{new_filename} 处理后数据数量: {len(filtered_data)}")

        except json.JSONDecodeError as e:
            print(f"读取 JSON 文件时出错: {filename} - 错误信息: {e}")
