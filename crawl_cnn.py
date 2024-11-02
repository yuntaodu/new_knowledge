import http.client, urllib.parse
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from datetime import datetime
import os

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
    # return article_content
    
    timestamp = return_text_if_not_none(soup.find('div', {'class': 'timestamp'}))
    
    if timestamp:
        timestamp = parse_timestamp(timestamp)
    else:
        timestamp = ['', '', '', '']
        
    all_images = soup.find_all('img', {'class': 'image__dam-img'}, src=True)

    # all_img_srcs = ''
    if all_images:
        all_img_srcs = [x['src'] for x in all_images if x['src']]
        all_img_cap = [x['alt'] for x in all_images if x['src']]
        # all_img_srcs = '\n'.join(all_img_srcs)

    # return all_img_srcs
    return title, author, article_content, timestamp, all_img_srcs, all_img_cap

def get_current_page(url = 'https://edition.cnn.com/2024/10/23/food/campbells-goldfish-name-change/index.html'):
    response = requests.get(url)
    data = response.text
    res = parse(data)

    title = res[0]
    author = res[1]
    time = res[3]

    ##
    content = res[2]
    content = content.split("\xa0—\xa0\n")[1].lstrip("\n ").strip()
    cont_list = content.split("\n\n")

    new_cont = []
    for index, da in enumerate(cont_list):
        if index == 0:
            new_cont.append(da)
            continue
        if da == "":
            continue
        if index != 0 and da[0] != " ":
            if da[0] != "\n":
                continue
            if da[5] == " " and da[10] == " " and  da[13] != " ":
                new_cont.append(da)
                continue
            else:
                continue 
        new_cont.append(da)

    ##
    all_imgs = res[4]
    all_desp = res[5]

    new_imgs = []
    new_desp = []
    for img, desp in zip(all_imgs, all_desp):
        if img.find("h_144,w_256") > -1:
            continue
        else:
            new_imgs.append(img)
            new_desp.append(desp)    

    # print(title)
    # print(author)
    # print(time)
    # print(new_cont)
    # print(new_imgs)
    # print(new_desp)
    
    return title, author, time, new_cont, new_imgs, new_desp






# import requests
# from bs4 import BeautifulSoup

def url_is_article(url, cur_type, current_year='2024'):
    if url:
        if 'cnn.com/{}/'.format(current_year) in url:
            if 'cnn.com/{}/'.format(current_year) in url and '/gallery/' not in url:
                return True
    return False


# 将新的数据追加到 JSONL 文件中
def append_to_jsonl_file(file_path, new_data):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(json.dumps(new_data, ensure_ascii=False) + '\n')


# 读取 JSONL 文件内容
def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))  # 解析每一行的 JSON 数据
    return data

def get_real_time():
    all_exit = 0
    all_success = 0
    all_fail = 0

    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
    current_day = formatted_now.split(" ")[0]
    current_year = current_day.split("-")[0]

    url_all_file_path = "all_url.jsonl"
    all_previous_url = read_jsonl_file(url_all_file_path)

    statis_path = "statil.jsonl"

    candicate = ['world', 'politics', 'business', 'health', 'entertainment', 'style', 'travel', 'sports', 'science', 'climate', 'weather']

    for current_type in candicate:
        
        count_type_exit = 0
        count_type_success = 0
        count_type_fail = 0
        
        today_file = "news/{}/{}.jsonl".format(current_day, current_type)
        today_folder = "news/{}".format(current_day)
        os.makedirs(today_folder, exist_ok=True)
        
        all_urls = []
        url = 'https://edition.cnn.com/{}'.format(current_type)
        url_combine = 'https://edition.cnn.com'
        data = requests.get(url).text
        soup = BeautifulSoup(data, features="html.parser")
        for a in soup.find_all('a', href=True):
            if a['href'] and a['href'][0] == '/' and a['href'] != '#':
                a['href'] = url_combine + a['href']
            all_urls.append(a['href'])
            
        article_urls = [url for url in all_urls if url_is_article(url, current_type, current_year)]
        all_data = []
        article_urls_duplicates_removed = list(set(article_urls))
        for count, article_url in enumerate(article_urls_duplicates_removed):
            if article_url in all_previous_url:
                # print("this areticle alreasy exists!")
                print("already exiet: ", current_type, count)
                count_type_exit = count_type_exit + 1
                continue         
            else:
                try:
                    append_to_jsonl_file(url_all_file_path, article_url)
                    title, author, time, new_cont, new_imgs, new_desp = get_current_page(article_url)
                    temp_item = {
                    'title' : title,
                    'author' : author,
                    'time' : time,
                    'new_cont' : new_cont,
                    'new_imgs' : new_imgs,
                    'new_desp' : new_desp   
                    }
                    append_to_jsonl_file(today_file, temp_item)
                    count_type_success = count_type_success + 1
                    print("success: ", current_type, count)
                except:
                    count_type_fail = count_type_fail + 1
                    print("error: ", current_type, count)
                    continue
        all_exit = all_exit + count_type_exit
        all_success = all_success + count_type_success
        all_fail = all_fail + count_type_fail   
        append_to_jsonl_file(statis_path, {"current_day" : current_day, "current_type" : current_type, "statis" : (count_type_exit, count_type_success, count_type_fail)}) 
    append_to_jsonl_file(statis_path, {"current_day" : current_day, "current_type" : "all", "all_statis" : (all_exit, all_success, all_fail)}) 
    
    
def get_past():
    
    conn = http.client.HTTPConnection('api.mediastack.com')

    params = urllib.parse.urlencode({
        'access_key': 'fc26ec92f04388a28ec066c75cdbcecf',
        'sources': 'cnn', #'cnn,-bbc',
        # 'countries': 'au,-us', 
        'date' : "2024-10-15,2024-10-22",
        # 'keywords' : 'hello',
        'languages' : 'en',
        'categories': 'sports', #'-general,-sports',
        'sort': 'published_desc',
        'offset' : 0,
        'limit': 2,
        })

    conn.request('GET', '/v1/news?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    json_data = json.loads(data.decode('utf-8'))
    print(json_data)

    # for da in json_data['data']:
    #     title, author, time, new_cont, new_imgs, new_desp = get_current_page(da['url'])
    #     a = 1
        
        
        
