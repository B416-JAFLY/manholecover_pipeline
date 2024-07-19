import os
import re
import json
from PIL import Image
from mmpretrain import get_model
from mmpretrain import ImageClassificationInferencer

# 加载分类模型
model_unit = get_model("cover_F&U_classification_model/vit-base-p16_1xb128-coslr-ft_custom_unit.py", pretrained="cover_F&U_classification_model/unit.pth")
model_funct = get_model("cover_F&U_classification_model/vit-base-p16_1xb128-coslr-ft_custom_funct.py", pretrained="cover_F&U_classification_model/funct.pth")

# 加载推理器
inferencer_unit = ImageClassificationInferencer(model_unit)
inferencer_funct = ImageClassificationInferencer(model_funct)

# 定义函数处理目录中的文件
def process_directory(path):
    pattern = re.compile(r"manhole_\d+\.jpg$")
    
    # 筛选出所有符合条件的图片文件
    image_files = [f for f in os.listdir(path) if pattern.search(f)]
    
    for image_file in image_files:
        image_path = os.path.join(path, image_file)
        json_file_path = image_path.replace('.jpg', '.json')
        
        print(f"Processing image: {image_file}")
        
        # 读取JSON文件
        with open(json_file_path, 'r') as json_file:
            json_data = json.load(json_file)
        
        # 读取图片
        image = Image.open(image_path)

        # 初始化功能区列表
        functional_areas = []
        unit_areas = []
        
        # 处理单位区
        for unit in json_data["unit"]:
            coordinates = unit["coordinates"]
            cropped_image = image.crop((coordinates["x1"], coordinates["y1"], coordinates["x2"], coordinates["y2"]))
            cropped_image_path = f"/tmp/unit_{coordinates['x1']}_{coordinates['y1']}.jpg"
            cropped_image.save(cropped_image_path)
            
            # 使用模型识别单位区图片块
            result_unit = inferencer_unit(cropped_image_path)[0]
            unit["class"] = result_unit["pred_class"]
            unit_areas.append(unit)
        
        # 处理功能区
        for funct in json_data["functional"]:
            coordinates = funct["coordinates"]
            cropped_image = image.crop((coordinates["x1"], coordinates["y1"], coordinates["x2"], coordinates["y2"]))
            cropped_image_path = f"/tmp/funct_{coordinates['x1']}_{coordinates['y1']}.jpg"
            cropped_image.save(cropped_image_path)
            
            # 使用模型识别功能区
            result_funct = inferencer_funct(cropped_image_path)[0]
            funct["class"] = result_funct["pred_class"]
            functional_areas.append(funct)
        
        # 更新JSON文件中的functional和unit里的每个元素的class字段
        json_data["functional"] = functional_areas
        json_data["unit"] = unit_areas
        
        # 保存更新后的JSON文件，确保中文字符不被转义
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        
        print(f"Updated JSON file: {json_file_path}")

# 指定目录路径
directory_path = "jpg_init_test"

# 处理目录
process_directory(directory_path)
