from http import HTTPStatus
import dashscope
import os
import json
from tqdm import tqdm

def simple_multimodal_conversation_call_construction(image_path):
    messages = [
        {
            "role": "user",
            "content": [
                {"image": image_path},
                {"text": "观察这张图片，图片中是否存在施工的情形？如果存在，回复1；如果不存在，回复0。回复中只要有0和1就可以，不要有其他文字。"}
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
    
def process_images_in_directory_construction(directory_path):
    image_files = [f for f in os.listdir(directory_path) if f.endswith("_ahead.jpg")]
    
    for filename in tqdm(image_files, desc="Processing Images"):
        image_path = os.path.join(directory_path, filename)
        result = simple_multimodal_conversation_call_construction(image_path)
        
        if result is not None:
            # 处理_ahead.json文件
            ahead_json_filename = os.path.splitext(filename)[0] + '.json'
            ahead_json_path = os.path.join(directory_path, ahead_json_filename)
            
            if os.path.exists(ahead_json_path):
                with open(ahead_json_path, 'r') as json_file:
                    data = json.load(json_file)
            else:
                data = {}

            data['construction'] = result

            with open(ahead_json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            # 处理_below.json文件
            below_json_filename = ahead_json_filename.replace("_ahead.json", "_below.json")
            below_json_path = os.path.join(directory_path, below_json_filename)
            
            if os.path.exists(below_json_path):
                with open(below_json_path, 'r') as json_file:
                    below_data = json.load(json_file)
            else:
                below_data = {}

            below_data['construction'] = result

            with open(below_json_path, 'w') as json_file:
                json.dump(below_data, json_file, indent=4)

images_directory = "jpg_init_test"
process_images_in_directory_construction(images_directory)