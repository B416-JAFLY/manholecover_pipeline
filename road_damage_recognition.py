from http import HTTPStatus
import dashscope
import os
import json
from tqdm import tqdm

def simple_multimodal_conversation_call_road_damage(image_path):
    messages = [
        {
            "role": "user",
            "content": [
                {"image": image_path},
                {"text": "观察这张图片，图片中是否存在道路破损的情形？如果存在，回复1；如果不存在，回复0。回复中只要有0和1就可以，不要有其他文字。"}
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
    
def process_images_in_directory_road_damage(directory_path):
    image_files = [f for f in os.listdir(directory_path) if f.endswith("_below.jpg")]
    
    for filename in tqdm(image_files, desc="Processing Images"):
        image_path = os.path.join(directory_path, filename)
        result = simple_multimodal_conversation_call_road_damage(image_path)
        
        if result is not None:
            json_filename = os.path.splitext(filename)[0] + '.json'
            json_path = os.path.join(directory_path, json_filename)
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)
            else:
                data = {}

            data['road_damage'] = result

            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

images_directory = "/home/u2021213565/jupyterlab/alibaba_qwen/jpg_init_test"
process_images_in_directory_road_damage(images_directory)