import os
import json
import re

def process_json_files(input_folder, output_folder):
    # 检查输出文件夹是否存在，不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            input_file_path = os.path.join(input_folder, filename)
            
            # 在文件名前加上"clean_"
            output_file_path = os.path.join(output_folder, f"clean_{filename}")

            with open(input_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 处理数据
            processed_data = []
            for entry in data:
                content = entry.get("content", [])
                
                # 检查 content 是否为空列表或仅包含空字符串，如果是则跳过该条数据
                if not content or all(line == "" for line in content):
                    continue
                
                # 处理包含“CNN —”的情况
                new_content = []
                for line in content:
                    if "CNN —" in line:
                        # 删除 "CNN —" 及其之前的内容
                        line = re.sub(r'^.*?CNN — ', '', line)
                    new_content.append(line)

                # 更新内容并添加到结果数据中
                entry["content"] = new_content
                processed_data.append(entry)

            # 将处理后的数据写入新的 JSON 文件
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(processed_data, f, ensure_ascii=False, indent=4)

    print("所有文件处理完成并保存至:", output_folder)

# 使用示例
input_folder = '/home/jiangkailin/project/New_Knowledge/content_2024'  # 替换为您的文件夹路径
output_folder = '/home/jiangkailin/project/New_Knowledge/clean_content'  # 新的文件夹路径
process_json_files(input_folder, output_folder)





