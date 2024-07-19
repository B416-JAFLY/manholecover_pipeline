import os
import re
import json
from ultralytics import YOLO

# 加载YOLO模型
model = YOLO("cover_F&U_detection_model/weights/best.pt")

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
        
        # 使用模型识别功能区
        results = model([image_path])
        
        # 初始化功能区列表
        functional_areas = []
        unit_areas = []
        
        for result in results:
            print(f"Detected {len(result.boxes)} objects in {image_file}")
            print(f"Result boxes: {result.boxes}")
            for box, cls in zip(result.boxes.xyxy.tolist(), result.boxes.cls.tolist()):
                print(f"Box: {box}, Class: {cls}")  # 添加调试信息
                x1, y1, x2, y2 = map(int, box)
                area_data = {
                    "class": -1,
                    "coordinates": {
                        "x1": x1,
                        "y1": y1,
                        "x2": x2,
                        "y2": y2
                    }
                }
                if cls == 0:  # 类别0对应manhole_cover_unit_area
                    unit_areas.append(area_data)
                elif cls == 1:  # 类别1对应manhole_cover_functional_area
                    functional_areas.append(area_data)
        
        # 打印检测结果
        print(f"Functional areas: {functional_areas}")
        print(f"Unit areas: {unit_areas}")
        
        # 更新JSON文件中的functional和unit字段
        json_data["functional"] = functional_areas
        json_data["unit"] = unit_areas
        
        # 保存更新后的JSON文件
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        
        print(f"Updated JSON file: {json_file_path}")

# 指定目录路径
directory_path = "jpg_init_test"

# 处理目录
process_directory(directory_path)
