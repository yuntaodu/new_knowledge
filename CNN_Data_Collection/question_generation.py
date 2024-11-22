import base64
from openai import AzureOpenAI
import json
import re
import os
from prompt import get_question_generation
from tqdm import tqdm

REGION = "eastus"
MODEL = "gpt-4o-2024-08-06"
# MODEL = "gpt-4o-mini-2024-07-18"
API_KEY = "5db570a2433b1179488e910840fe60ee"
API_BASE = "https://api.tonggpt.mybigai.ac.cn/proxy"
ENDPOINT = f"{API_BASE}/{REGION}"

client = AzureOpenAI(
    api_key=API_KEY,
    api_version="2024-09-01-preview",
    azure_endpoint=ENDPOINT,
)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


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

def filter_imgs():

    input_file = "/home/jiangkailin/project/New_Knowledge/entity_json/filter_imgs_gpt4o_mini.json"
    output_file = "/home/jiangkailin/project/New_Knowledge/entity_json/EUQA_mini_2_4o.json"
    
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found.")
        return

    json_data = read_json_file(input_file)
    print(f"Processing {len(json_data)} news items from {input_file}")

    
    for index, da in enumerate(tqdm(json_data, desc="Processing JSON items")):
        

        system_prompt, example_1_input, example_1_output = get_question_generation()

        full_system_prompt = f"{system_prompt}\n{example_1_input}\n{example_1_output}\n"

        entitys = ', '.join(da['Entitys'])
    
        prompt = "title: {}\nContent: {}\nEntitys: {}".format(da['title'], da['Summary'],entitys)

      
        res = get_chatgpt_response(full_system_prompt, prompt)

        # pattern = r"(Entity\d+): (.*?)\n(Upper\d+): (.*?)\n(Question\d+): (.*?)\n(Answer\d+): (.*?)\n"
        # matches = re.findall(pattern, res)
        # print(res)


        # output = {}
        # for match in matches:
        #     entity, entity_val, upper, upper_val, question, question_val, answer, answer_val = match
        #     entry_key = f"EUQA{entity[6:]}"
        #     output[entry_key] = {
        #         entity: entity_val,
        #         upper: upper_val,
        #         question: question_val,
        #         answer: answer_val,
        #     }


        pattern = r"(Entity\d+): (.*?)\s+Upper\d+: (.*?)\s+Question\d+: (.*?)\s+Answer\d+: (.*?)(?=\n\n|$)"
        matches = re.findall(pattern, res)

        # 组织成所需的输出格式
        output = {"EUQA": {}}
        for match in matches:
            entity, entity_val, upper_val, question_val, answer_val = match
            entry_key = f"EUQA{entity[6:]}"
            output["EUQA"][entry_key] = {
                entity: entity_val.strip(),
                f"Upper{entity[6:]}": upper_val.strip(),
                f"Question{entity[6:]}": question_val.strip(),
                f"Answer{entity[6:]}": answer_val.strip()
            }
        print(res)


        # da['EUQA'] = output
        da.update(output)
        
        append_to_json_file(output_file, da)
        print(f"Finished processing item {index}.")
   
   
filter_imgs()
