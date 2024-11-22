import json
import os
from openai import AzureOpenAI
from prompt import get_summ_2_prompt,get_summ_prompt


REGION = "eastus"
MODEL = "gpt-4o-2024-08-06"
API_KEY = "5db570a2433b1179488e910840fe60ee"
API_BASE = "https://api.tonggpt.mybigai.ac.cn/proxy"
ENDPOINT = f"{API_BASE}/{REGION}"

client = AzureOpenAI(
    api_key=API_KEY,
    api_version="2024-09-01-preview",
    azure_endpoint=ENDPOINT,
)


def get_chatgpt_response(system_prompt, prompt):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        model=MODEL,
    )
    return response.choices[0].message.content

def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  
            if not isinstance(data, list):
                print("Error: JSON data is not an array format")
                return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
    

    return data



def append_to_json_file(file_path, new_data):

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([new_data], file, ensure_ascii=False, indent=4)
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            if not isinstance(data, list):
                print("Error: JSON data is not in array format.")
                return
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON.")
            return


    data.append(new_data)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_summary():
    input_file = "/home/jiangkailin/project/New_Knowledge/test_content.json"
    output_file = "/home/jiangkailin/project/New_Knowledge/entity_json/summary_test_content.json"
    
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    current_json_data = read_json_file(input_file)
    print(f"Processing {len(current_json_data)} news items from {input_file}")
    

    for index, da in enumerate(current_json_data):

        # system_prompt = get_summ_2_prompt()
        system_prompt = get_summ_prompt()
        
        prompt_content = " ".join(da['content'])
        prompt = f"title: {da['title']}\nContent: {prompt_content}"
        
        res = get_chatgpt_response(system_prompt, prompt)
        

        # summary = res.split("Objects:")[0].split("Summarized:")[1].strip()
        # object = res.split("Objects:")[1].strip()
        # objects = [term.strip() for term in object.split(",")]
        # da['summary'] = summary
        # da['objects'] = objects


        Summary = res.split("Entitys:")[0].split("Summarized:")[1].strip()
        Entity = res.split("Entitys:")[1].strip()
        Entitys = [term.strip() for term in Entity.split(",")]
        da['Summary'] = Summary
        da['Entitys'] = Entitys
        
        append_to_json_file(output_file, da)
        print(f"finsh processing item {index}.")


get_summary()
