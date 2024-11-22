import requests
from bs4 import BeautifulSoup
import os
import json
import time

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

def is_valid_image(image_data):
    if len(image_data) < 10:
        return False

    if image_data.startswith(b'\xFF\xD8\xFF'):  
        return True
    elif image_data.startswith(b'\x89PNG'):     
        return True
    elif image_data.startswith(b'GIF89a') or image_data.startswith(b'GIF87a'):  
        return True
    return False

def download_images(search_term, num_images, save_path, retries=3):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    url = f'https://www.bing.com/images/search?q={search_term}&form=HDRSC2&first=1&tsc=ImageBasicHover'
    html = requests.get(url, headers=header).text
    soup = BeautifulSoup(html, 'html.parser')
    img_tags = soup.find_all('a', {'class': 'iusc'})

    img_urls = []
    for img in img_tags:
        if len(img_urls) >= num_images:
            break
        m = img.get('m')
        if m:
            try:
                m_json = json.loads(m)
                img_urls.append(m_json['murl'])
            except json.JSONDecodeError as e:
                print(f"JSONDecodeError when parsing 'm' attribute: {e}")
                continue

    for i, img_url in enumerate(img_urls):
        for attempt in range(retries):
            try:
                img_data = requests.get(img_url, timeout=10).content
                if not is_valid_image(img_data):
                    print(f"Invalid image format for URL: {img_url}")
                    break  

                img_name = f"{search_term.replace(' ', '_')}_{i + 1}.jpg"
                img_path = os.path.join(save_path, img_name)
                with open(img_path, 'wb') as handler:
                    handler.write(img_data)
                print(f"Downloaded {img_name} to {img_path}")
                break
            except (requests.ConnectionError, requests.Timeout) as e:
                print(f"Attempt {attempt + 1} - Connection error for {img_url}: {e}")
                time.sleep(2)
            except Exception as e:
                print(f"Attempt {attempt + 1} - Could not download {img_url}: {e}")
                time.sleep(2)
        else:
            print(f"Failed to download {img_url} after {retries} attempts")

def process_json(json_path, root_save_path):
    with open(json_path, 'r') as file:
        data_list = json.load(file)

    for data in data_list:
        id_value = data.get("id")
        euqa_data = data.get("EUQA")
        
        if not id_value or not euqa_data:
            print("Missing 'id' or 'EUQA' field.")
            continue
        
        for i in range(1, 5):
            entity_key = f"Entity{i}"
            Upper_key = f"Upper{i}"
            euqa_key = f"EUQA{i}"
            entity_name = euqa_data.get(euqa_key, {}).get(entity_key)
            Upper_name = euqa_data.get(euqa_key, {}).get(Upper_key)
            name = entity_name + ' ' + Upper_name
            
            if entity_name:
                save_path = os.path.join(root_save_path, f"CNN_EUQA_{id_value}", euqa_key)
                download_images(name, 15, save_path)
            else:
                print(f"Entity {i} not found in {id_value}.")

if __name__ == '__main__':
    json_path = '/home/jiangkailin/project/New_Knowledge/entity_json/EUQA_mini_2_4o_index.json'
    root_save_path = '/home/jiangkailin/project/New_Knowledge/CNN_EUQA'
    process_json(json_path, root_save_path)




# import requests
# from bs4 import BeautifulSoup
# import os
# import json
# import time

# header = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# }

# def download_images(search_term, num_images, save_path, retries=3):
#     if not os.path.exists(save_path):
#         os.makedirs(save_path)

#     url = f'https://www.bing.com/images/search?q={search_term}&form=HDRSC2&first=1&tsc=ImageBasicHover'
#     html = requests.get(url, headers=header).text
#     soup = BeautifulSoup(html, 'html.parser')
#     img_tags = soup.find_all('a', {'class': 'iusc'})

#     img_urls = []
#     for img in img_tags:
#         if len(img_urls) >= num_images:
#             break
#         m = img.get('m')
#         if m:
#             try:
#                 m_json = json.loads(m)
#                 img_urls.append(m_json['murl'])
#             except json.JSONDecodeError as e:
#                 print(f"JSONDecodeError when parsing 'm' attribute: {e}")
#                 continue

#     for i, img_url in enumerate(img_urls):
#         for attempt in range(retries):
#             try:
#                 img_data = requests.get(img_url, timeout=10).content
#                 img_name = f"{search_term.replace(' ', '_')}_{i + 1}.jpg"
#                 img_path = os.path.join(save_path, img_name)
#                 with open(img_path, 'wb') as handler:
#                     handler.write(img_data)
#                 print(f"Downloaded {img_name} to {img_path}")
#                 break
#             except (requests.ConnectionError, requests.Timeout) as e:
#                 print(f"Attempt {attempt + 1} - Connection error for {img_url}: {e}")
#                 time.sleep(2)
#             except Exception as e:
#                 print(f"Attempt {attempt + 1} - Could not download {img_url}: {e}")
#                 time.sleep(2)
#         else:
#             print(f"Failed to download {img_url} after {retries} attempts")

# def process_json(json_path, root_save_path):
#     with open(json_path, 'r') as file:
#         data_list = json.load(file)

#     for data in data_list:
#         id_value = data.get("id")
#         euqa_data = data.get("EUQA")

        
#         if not id_value or not euqa_data:
#             print("Missing 'id' or 'EUQA' field.")
#             continue
        
#         for i in range(1, 5):
#             entity_key = f"Entity{i}"
#             Upper_key = f"Upper{i}"
#             euqa_key = f"EUQA{i}"
#             entity_name = euqa_data.get(euqa_key, {}).get(entity_key)
#             Upper_name = euqa_data.get(euqa_key, {}).get(Upper_key)
#             name = entity_name + ' ' + Upper_name
            
#             if entity_name:
#                 save_path = os.path.join(root_save_path, f"{id_value}_EUQA", euqa_key, entity_name)
#                 download_images(name, 15, save_path)
#             else:
#                 print(f"Entity {i} not found in {id_value}.")

# if __name__ == '__main__':
#     json_path = '/home/jiangkailin/project/New_Knowledge/entity_json/EUQA_mini_2_4o_index.json'
#     root_save_path = '/home/jiangkailin/project/New_Knowledge/CNN_EUQA'
#     process_json(json_path, root_save_path)
