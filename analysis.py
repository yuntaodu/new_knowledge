import json
import os
import openai
from prompt import get_summ_chin_prompt, get_score_prompt, get_match_score
import base64
import requests
# from openai import AzureOpenAI
# REGION = "westus"
# MODEL = "o1-mini-2024-09-12"
# API_KEY = "63e53e39d28006263778db51d841f49a"
# API_BASE = "https://api.tonggpt.mybigai.ac.cn/proxy"
# ENDPOINT = f"{API_BASE}/{REGION}"
# client = AzureOpenAI(
#     api_key=API_KEY,
#     api_version="2024-09-01-preview",
#     azure_endpoint=ENDPOINT,
# )

# def get_chatgpt_response(system_prompt, prompt):
#     # print(input)
#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {
#                 "role": "system",
#                 "content": system_prompt
#             },
#             {"role": "user", "content": prompt}
#         ],
#     )
#     return response.choices[0].message.content



from openai import OpenAI

client = OpenAI(
    base_url='https://api.openai-proxy.org/v1',
    api_key='sk-ifaeShm4AUoohgWo7ur4YpOBs2yaGj7p8I29PEy1niAHCDk5',
)

def get_chatgpt_response(system_prompt, prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o-mini",
    )
    return response.choices[0].message.content


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


def get_chatgpt_response_img(system_prompt, prompt, base64_image):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {"role": "user", 
             "content": [
                    {
                    "type": "text",
                    "text": prompt,
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url":  f"data:image/jpeg;base64,{base64_image}"
                    },
                    },
                ],
            }
        ],
        model="gpt-4o-mini",
    )
    return response.choices[0].message.content

def append_to_jsonl_file(file_path, new_data):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(json.dumps(new_data, ensure_ascii=False) + '\n')


def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))  # 解析每一行的 JSON 数据
    return data

def get_summary_chinese():
    for current_day in ["2024-10-25", "2024-10-26", "2024-10-28"]:
        for current_type in ['world', 'politics', 'business', 'health', 'entertainment', 'style', 'travel', 'sports', 'science', 'climate', 'weather']:
            current_file = os.path.join("news", current_day, current_type+".jsonl")
            if not os.path.exists(current_file):
                continue
            out_file = os.path.join("news", current_day, current_type+"_summarized.jsonl")
            if os.path.exists(out_file):
                continue
            current_json_data = read_jsonl_file(current_file)
            print(current_day, current_type, len(current_json_data))
            for index, da in enumerate(current_json_data):
                try:
                    system_prompt = get_summ_chin_prompt()
                    # system_prompt = "You are a helpful assistant. Please help me summarize the news into a new description less then 100 words. You are given the new title and news content. Besides, you need to translate the summarized description into chinese. The output format is 'summrized: #summarized description. \n chinese: #the chinese of summarized desciption.'"
                    temp_cont = []
                    for cont in da['new_cont']:
                        if cont[8] == " ":
                            temp_cont.append(cont.strip())
                        else:
                            temp_cont.append("\n" + cont.strip())
                    prompt = "title : {}\nContent : {}".format(da['title'], "\n".join(temp_cont))
                    
                    res = get_chatgpt_response(system_prompt, prompt)
                    summ = res.split("Chinese:")[0].split("Summarized:")[1].strip()
                    chinese = res.split("Chinese:")[1].strip()
                    da['summ'] = summ
                    da['chinese'] = chinese
                    da['show'] = "\n".join(temp_cont)
                    append_to_jsonl_file(out_file, da)
                except:
                    print("error in {}, {}, {}.".format(current_day, current_type, index))
                    
def news_importance_score():        
    for current_day in ["2024-10-25", "2024-10-26", "2024-10-28"]:
        for current_type in ['world', 'politics', 'business', 'health', 'entertainment', 'style', 'travel', 'sports', 'science', 'climate', 'weather']:
        # for current_type in ['business',  'sports', 'science', 'climate', 'weather']:
            current_file = os.path.join("news", current_day, current_type+"_summarized.jsonl")
            if not os.path.exists(current_file):
                continue
            out_file = os.path.join("news", current_day, current_type+"_summarized_score.jsonl")
            if os.path.exists(out_file):
                continue
            current_json_data = read_jsonl_file(current_file)
            print(current_day, current_type, len(current_json_data))
            for index, da in enumerate(current_json_data):
                try:
                    system_prompt = get_score_prompt()
                    # temp_cont = []
                    # for cont in da['new_cont']:
                    #     if cont[8] == " ":
                    #         temp_cont.append(cont.strip())
                    #     else:
                    #         temp_cont.append("\n" + cont.strip())
                    prompt = "title: {}\nContent: {}".format(da['title'], da['summ'])
                    
                    res = get_chatgpt_response(system_prompt, prompt)
                    # da['show'] = "\n".join(temp_cont)
                    da['score'] = int(res.split("Score:")[1].split("Reason")[0].strip())
                    da['reason'] = res.split("Reason:")[1].strip()
                    print(da['score'])
                    append_to_jsonl_file(out_file, da)
                except:
                    print("error in {}, {}, {}.".format(current_day, current_type, index))



def download_img():        
    for current_day in ["2024-10-25", "2024-10-26", "2024-10-28"]:
        for current_type in ['world', 'politics', 'business', 'health', 'entertainment', 'style', 'travel', 'sports', 'science', 'climate', 'weather']:
            current_file = os.path.join("news", current_day, current_type+"_summarized_score.jsonl")
            if not os.path.exists(current_file):
                continue
            out_file = os.path.join("news", current_day, current_type+"_summarized_score_real_img.jsonl")
            if os.path.exists(out_file):
                continue
            current_json_data = read_jsonl_file(current_file)
            print(current_day, current_type, len(current_json_data))
            for index, da in enumerate(current_json_data):
                local_img_path = []
                for index_img, img in enumerate(da['new_imgs']):
                    try:
                        response = requests.get(img) #.split("?")[0])
                        os.makedirs(os.path.join("imgs", current_day, current_type), exist_ok=True)
                        with open(os.path.join("imgs", current_day, current_type, str(index) + "_" + str(index_img) + ".png"), 'wb') as f:
                            f.write(response.content)    
                        local_img_path.append(os.path.join("imgs", current_day, current_type, str(index) + "_" + str(index_img) + ".png"))
                    except:
                        print("error in {}, {}, {}.".format(current_day, current_type, index))
                da['local_img_path'] = local_img_path
                append_to_jsonl_file(out_file, da)


def check():
    for current_day in ["2024-10-25",]: # "2024-10-26", "2024-10-28"]:
        for current_type in ['world', 'politics', 'business', 'health', 'entertainment', 'style', 'travel', 'sports', 'science',]: # 'climate', 'weather']:
            current_file = os.path.join("news", current_day, current_type+"_summarized.jsonl")
            if not os.path.exists(current_file):
                continue
            current_json_data = read_jsonl_file(current_file)
            len1 = len(current_json_data)
            
            current_file = os.path.join("news", current_day, current_type+"_summarized_score.jsonl")
            if not os.path.exists(current_file):
                continue
            current_json_data = read_jsonl_file(current_file)
            len2 = len(current_json_data)
            
            current_file = os.path.join("news", current_day, current_type+"_summarized_score_real_img.jsonl")
            if not os.path.exists(current_file):
                continue
            current_json_data = read_jsonl_file(current_file)
            len3 = len(current_json_data)
            
            current_file = os.path.join("news", current_day, current_type+".jsonl")
            if not os.path.exists(current_file):
                continue
            current_json_data = read_jsonl_file(current_file)
            len4 = len(current_json_data)
            print(len1, len2, len3, len4)


def match_score():        
    for current_day in ["2024-10-25",]: # "2024-10-26", "2024-10-28"]:
        # for current_type in ['world', 'politics', 'business', 'health', 'entertainment', 'style', 'travel', 'sports', 'science',]: # 'climate', 'weather']:\
        for current_type in ['sports']:
            current_file = os.path.join("news", current_day, current_type+"_summarized_score_real_img.jsonl")
            if not os.path.exists(current_file):
                continue
            out_file = os.path.join("news", current_day, current_type+"_summarized_score_real_img_match.jsonl")
            if os.path.exists(out_file):
                continue
            current_json_data = read_jsonl_file(current_file)
            print(current_day, current_type, len(current_json_data))
            for index, da in enumerate(current_json_data):
                match_score = {}
                match_reason = {} 
                for index_img, (img, cap) in enumerate(zip(da['local_img_path'], da['new_desp'])):
                    try:
                        system_prompt = get_match_score()
                        prompt = "title: {}\nContent: {}\nImage caption: {}".format(da['title'], da['summ'], cap)   
                        base64_img = encode_image(img)
                        res = get_chatgpt_response_img(system_prompt, prompt, base64_img)
                        match_score[img] = int(res.split("Score:")[1].split("Reason")[0].strip())
                        match_reason[img] = res.split("Reason:")[1].strip()
                        # print(da['match_score'])
                    except:
                        print("error in {}, {}, {}.".format(current_day, current_type, index))
                da['match_score'] = match_score
                da['match_reason'] = match_reason
                append_to_jsonl_file(out_file, da)

def for_show():
    
    all_candicate = []
    for current_day in ["2024-10-25",  "2024-10-26", "2024-10-28"]:
        for current_type in ['world', 'politics', 'business', 'health', 'entertainment', 'style', 'travel', 'sports', 'science', 'climate', 'weather']:
            current_file = os.path.join("news", current_day, current_type+"_summarized_score_real_img_match.jsonl")
            if not os.path.exists(current_file):
                continue
            out_file_sel = os.path.join("news", "show_sel.jsonl")
            out_file_not_sel = os.path.join("news", "show_unsel.jsonl")
            out_file_best = os.path.join("news", "show_best.jsonl")
            out_file_worst = os.path.join("news", "show_worst.jsonl")
            current_json_data = read_jsonl_file(current_file)
            print(current_day, current_type, len(current_json_data))
            temp_sel = []
            temp_not_sel = []
            for index, da in enumerate(current_json_data):
                if len(da['match_score']) == 0 or len(da['match_reason']) == 0:
                    continue
                else:
                    # print(da['score'])
                    if da['score'] >= 8:
                        # print(da['score'])
                        temp_sel.append(da)
                    if da['score'] <= 5:
                        # print(da['score'])
                        temp_not_sel.append(da)
                
            for da in temp_sel:
                append_to_jsonl_file(out_file_sel, da)
                
            for da in temp_not_sel:
                append_to_jsonl_file(out_file_not_sel, da)
                
            for sel in temp_sel:
                for m_score_path in sel['match_score']:
                    all_candicate.append((sel, m_score_path, sel['match_score'][m_score_path]))
                    
    sorted_data = sorted(all_candicate, key=lambda x: x[2], reverse = True)
    for index, so_da in enumerate(sorted_data):
        if index > 10:
            break
        new_da = so_da[0]
        new_da['show_img'] = [so_da[1]]
        new_da['show_img_score'] = [so_da[2]]
        # new_da['show_cap'] = [so_da[3]]
        append_to_jsonl_file(out_file_best, new_da)
        
    for index, so_da in enumerate(sorted_data[::-1]):
        if index > 10:
            break
        new_da = so_da[0]
        new_da['show_img'] = [so_da[1]]
        new_da['show_img_score'] = [so_da[2]]
        # new_da['show_cap'] = [so_da[3]]
        append_to_jsonl_file(out_file_worst, new_da)


def for_show_all():
    
    # all_candicate = []
    all_object = []
    for current_day in ["2024-10-25",  "2024-10-26", "2024-10-28"]:
        for current_type in ['world', 'politics', 'business', 'health', 'entertainment', 'style', 'travel', 'sports', 'science', 'climate', 'weather']:
            current_file = os.path.join("news", current_day, current_type+"_summarized_score_real_img_match_main_object.jsonl")
            if not os.path.exists(current_file):
                continue
            out_file = os.path.join("news", "show_all.jsonl")
            current_json_data = read_jsonl_file(current_file)
            print(current_day, current_type, len(current_json_data))
            for index, da in enumerate(current_json_data):
                append_to_jsonl_file(out_file, da)
                all_object.append(da['main_object'])
    # print(all_object)    
    for ob in all_object:
        print(ob)      

                


def get_main_object():
    for current_day in ["2024-10-25",]: # "2024-10-26", "2024-10-28"]:
        for current_type in ['world', 'politics', 'business', 'health', 'entertainment', 'style', 'travel', 'sports', 'science',]: # 'climate', 'weather']:\
        # for current_type in ['sports']:
            current_file = os.path.join("news", current_day, current_type+"_summarized_score_real_img_match.jsonl")
            if not os.path.exists(current_file):
                continue
            out_file = os.path.join("news", current_day, current_type+"_summarized_score_real_img_match_main_object.jsonl")
            current_json_data = read_jsonl_file(current_file)
            print(current_day, current_type, len(current_json_data))
            for da in current_json_data:
                system_prompt = "You are given a news with the news title and title content, Please recongnize the main object of the news. Note that the main object should be a noun without containing verb. Output with less than five words."
                prompt = "title: {}\nContent: {}".format(da['title'], da['summ'])
                main_object = get_chatgpt_response(system_prompt, prompt)
                da['main_object'] = main_object
                append_to_jsonl_file(out_file, da)
# news_importance_score()
# download_img()
# check()
# match_score()

# for_show()



get_main_object()
for_show_all()