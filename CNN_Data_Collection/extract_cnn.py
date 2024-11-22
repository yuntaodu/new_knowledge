import json
import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

def return_text_if_not_none(element):
    if element:
        return element.text.strip()
    else:
        return ''

def parse_timestamp(timestamp):
    if 'Published' in timestamp:
        timestamp_type = 'Published'
    elif 'Updated' in timestamp:
        timestamp_type = 'Updated'
    else:
        timestamp_type = ''
    
    article_time, article_day, article_year = timestamp.replace('Published', '').replace('Updated', '').split(', ')
    return timestamp_type, article_time.strip(), article_day.strip(), article_year.strip()

def parse(html):
    soup = BeautifulSoup(html, features="html.parser")
    title = return_text_if_not_none(soup.find('h1', {'class': 'headline__text'}))
    author = soup.find('span', {'class': 'byline__name'})
    if not author:
        author = soup.find('span', {'class': 'byline__names'})
    author = return_text_if_not_none(author)
    
    article_content = return_text_if_not_none(soup.find('div', {'class': 'article__content'}))
    timestamp = return_text_if_not_none(soup.find('div', {'class': 'timestamp'}))
    
    if timestamp:
        timestamp = parse_timestamp(timestamp)
    else:
        timestamp = ['', '', '', '']
        
    all_images = soup.find_all('img', {'class': 'image__dam-img'}, src=True)
    if all_images:
        all_img_srcs = [x['src'] for x in all_images if x['src']]
        all_img_cap = [x['alt'] for x in all_images if x['src']]
    else:
        all_img_srcs, all_img_cap = [], []
        
    return title, author, article_content, timestamp, all_img_srcs, all_img_cap

def get_current_page(url):
    response = requests.get(url)
    data = response.text
    res = parse(data)

    title, author, time = res[0], res[1], res[3]
    content = res[2]

   
    content = content.replace("\xa0", " ").replace("\n", " ").strip()
    content = ' '.join(content.split())  

    
    content = content.replace('“', "'")
    content = content.replace('”', "'")

    
    content = [content]

    # 返回其他解析的数据
    all_imgs, all_desp = res[4], res[5]
    new_imgs, new_desp = [], []
    for img, desp in zip(all_imgs, all_desp):
        if img.find("h_144,w_256") == -1:
            new_imgs.append(img)
            new_desp.append(desp)

    return title, author, time, content, new_imgs, new_desp

# 将新的数据追加到 JSON 文件中，确保数据在一个列表内
def append_to_json_file(file_path, new_data):
    # 读取原始文件内容，如果文件不存在则创建一个空数组
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # 将新数据添加到现有数据列表中
    existing_data.extend(new_data)
    
    # 将完整数据写入文件，保持 JSON 数组格式
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

# 处理目录中的所有 JSON 文件
def process_json_files_in_directory(input_directory, output_directory, output_prefix="content_"):
    # 获取所有 JSON 文件并使用 tqdm 显示进度
    json_files = [f for f in os.listdir(input_directory) if f.endswith('.json')]
    for file_index, file_name in enumerate(tqdm(json_files, desc="Processing files", unit="file")):
        input_file = os.path.join(input_directory, file_name)
        output_file = os.path.join(output_directory, f"{output_prefix}{file_name}")
        process_urls_from_json(input_file, output_file, file_index + 1, len(json_files))

# 读取 JSON 文件并解析每个 URL
def process_urls_from_json(input_file, output_file, file_index, total_files):
    with open(input_file, 'r', encoding='utf-8') as file:
        url_data = json.load(file)
    
    news_items = []
    print(f"\nProcessing file {file_index}/{total_files}: {input_file}")
    for entry_index, entry in enumerate(tqdm(url_data, desc="Processing entries", unit="entry")):  # 限制每个文件处理 10 条记录
        url = entry.get("url")
        news_type = entry.get("type")
        time = entry.get("time")
        
        try:
            title, author, timestamp, content, images, descriptions = get_current_page(url)
            news_item = {
                "url": url,
                "type": news_type,
                "time": time,
                "title": title,
                "author": author,
                "timestamp": timestamp,
                "content": content,
                "images": images,
                "descriptions": descriptions
            }
            news_items.append(news_item)
            print(f"  Successfully processed entry {entry_index + 1}/{len(url_data[:10])}: {url}")
        except Exception as e:
            print(f"  Failed to process entry {entry_index + 1}/{len(url_data[:10])}: {url}, error: {e}")

    # 将所有的新闻数据保存到 JSON 文件中
    append_to_json_file(output_file, news_items)

# 使用示例
input_directory = "/home/jiangkailin/project/New_Knowledge/11.12/cnn_data/new2024"  # 输入文件夹路径
output_directory = "/home/jiangkailin/project/New_Knowledge/content_2024"  # 指定输出文件夹路径
process_json_files_in_directory(input_directory, output_directory)
