import os
import json
from PIL import Image
from ultralytics import YOLO

# 加载YOLO模型
model = YOLO("cover_recognition_model/weights/best.pt")

# 处理指定目录下的所有文件
def process_directory(path):
    for filename in os.listdir(path):
        if filename.endswith("_below.jpg"):
            # 获取文件的完整路径
            file_path = os.path.join(path, filename)
            json_file_path = file_path.replace('.jpg', '.json')
            
            # 读取json文件
            with open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)
            
            # 使用模型识别井盖
            results = model([file_path])
            
            # 更新json文件
            manhole_count = 0
            manhole_info = []
            for result in results:
                for i, box in enumerate(result.boxes.xyxy.tolist()):
                    manhole_count += 1
                    x1, y1, x2, y2 = map(int, box)
                    manhole_info.append({
                        "id": manhole_count,
                        "coordinates": {
                            "x1": x1,
                            "y1": y1,
                            "x2": x2,
                            "y2": y2
                        }
                    })
                    
                    # 裁剪并保存井盖图片
                    with Image.open(file_path) as img:
                        cropped_img = img.crop((x1, y1, x2, y2))
                        cropped_img_filename = f"{filename.replace('.jpg', '')}_manhole_{manhole_count}.jpg"
                        cropped_img_path = os.path.join(path, cropped_img_filename)
                        cropped_img.save(cropped_img_path)
                        
                        # 创建井盖图片的json文件
                        cropped_json_data = {
                            "filename": cropped_img_filename.replace('.jpg', ''),
                            "timestamp": json_data["timestamp"],
                            "gps": json_data["gps"],
                            "manhole_id": manhole_count,
                            "functional": {},
                            "unit": {}
                        }
                        cropped_json_file_path = cropped_img_path.replace('.jpg', '.json')
                        with open(cropped_json_file_path, 'w') as cropped_json_file:
                            json.dump(cropped_json_data, cropped_json_file, indent=4)
            
            # 更新原图的json文件
            json_data["quantity"] = manhole_count
            json_data["manhole"] = manhole_info
            with open(json_file_path, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)

# 指定目录路径
directory_path = "jpg_init_test"

# 处理目录
process_directory(directory_path)
