from http import HTTPStatus
import dashscope
import os
import json
from tqdm import tqdm

#export DASHSCOPE_API_KEY="sk-d181674e365c45fd8894065f8a1ed2ad"

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

def process_images_in_directory_construction(directory_path):
    image_files = [f for f in os.listdir(directory_path) if f.endswith(".jpg")]
    
    for filename in tqdm(image_files, desc="Processing Images"):
        image_path = os.path.join(directory_path, filename)
        result = simple_multimodal_conversation_call_construction(image_path)
        
        if result is not None:
            json_filename = os.path.splitext(filename)[0] + '.json'
            json_path = os.path.join(directory_path, json_filename)
            
            if os.path.exists(json_path):
                with open(json_path, 'r') as json_file:
                    data = json.load(json_file)
            else:
                data = {}

            data['construction'] = result

            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

def process_images_in_directory_road_damage(directory_path):
    image_files = [f for f in os.listdir(directory_path) if f.endswith(".jpg")]
    
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

def process_images_in_directory_defective_manhole(directory_path):
    image_files = [f for f in os.listdir(directory_path) if f.endswith(".jpg")]
    
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

if __name__ == '__main__':
    images_directory = "/home/u2021213565/jupyterlab/images_dataset_resnet"
    # process_images_in_directory_defective_manhole(images_directory)
    simple_multimodal_conversation_call_construction("/home/u2021213565/jupyterlab/images_dataset_resnet/2.jpg")
