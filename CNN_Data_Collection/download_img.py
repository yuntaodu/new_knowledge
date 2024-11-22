import json
import requests
import os


def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"下载成功: {filename}")
    else:
        print(f"下载失败: {url}")


with open('/home/jiangkailin/project/New_Knowledge/entity_json/summary_test_content.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


for news_index, item in enumerate(data, start=1):
    if 'images' in item:
        
        news_folder = f"/home/jiangkailin/project/New_Knowledge/cnn_test_img/cnn_{news_index}"
        
        os.makedirs(news_folder, exist_ok=True)
        
        for image_index, image_url in enumerate(item['images'], start=1):
            
            filename = os.path.join(news_folder, f"cnn_content_{news_index}_{image_index}.jpg")
            
            download_image(image_url, filename)
