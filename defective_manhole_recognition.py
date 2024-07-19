from http import HTTPStatus
import dashscope
import os
import json
from tqdm import tqdm
import re

def simple_multimodal_conversation_call_defective_manhole(image_path):
    messages = [
        {
            "role": "user",
            "content": [
                {"image": image_path},
                {"text": "观察这个井盖，井盖是否存在破损、丢失的情形？如果存在，回复1；如果不存在，回复0。回复中只要有0和1就可以，不要有其他文字。"}
            ]
        }
    ]
    response = dashscope.MultiModalConversation.call(model=dashscope.MultiModalConversation.Models.qwen_vl_chat_v1,
                                                     messages=messages)

    if response.status_code == HTTPStatus.OK:
        return response.output.choices[0].message.content
    else:
        print(f"Error code: {response.code}")
        print(f"Error message: {response.message}")
        return None

def process_images_in_directory_defective_manhole(directory_path):
    # 使用正则表达式筛选出目录中所有以manhole_x.jpg结尾的文件
    pattern = re.compile(r"manhole_\d+\.jpg$")
    image_files = [f for f in os.listdir(directory_path) if pattern.search(f)]

    # 打印筛选出的文件列表
    print(image_files)
    
    for filename in tqdm(image_files, desc="Processing Images"):
        image_path = os.path.join(directory_path, filename)
        result = simple_multimodal_conversation_call_defective_manhole(image_path)
        
        if result is not None:
            json_filename = os.path.splitext(filename)[0] + '.json'
            json_path = os.path.join(directory_path, json_filename)
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)
            else:
                data = {}

            data['defective_manhole'] = result

            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

images_directory = "jpg_init_test"
process_images_in_directory_defective_manhole(images_directory)