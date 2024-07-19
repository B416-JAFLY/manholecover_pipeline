import os
import json
import piexif
from PIL import Image
from datetime import datetime

def get_gps_info(exif_data):
    if piexif.GPSIFD.GPSLatitude in exif_data['GPS'] and piexif.GPSIFD.GPSLongitude in exif_data['GPS']:
        lat = exif_data['GPS'][piexif.GPSIFD.GPSLatitude]
        lon = exif_data['GPS'][piexif.GPSIFD.GPSLongitude]
        latitude = lat[0][0] / lat[0][1] + lat[1][0] / lat[1][1] / 60.0 + lat[2][0] / lat[2][1] / 3600.0
        longitude = lon[0][0] / lon[0][1] + lon[1][0] / lon[1][1] / 60.0 + lon[2][0] / lon[2][1] / 3600.0
        return {"latitude": latitude, "longitude": longitude}
    return {"latitude": 0, "longitude": 0}

def get_datetime_info(exif_data):
    if piexif.ExifIFD.DateTimeOriginal in exif_data['Exif']:
        datetime_str = exif_data['Exif'][piexif.ExifIFD.DateTimeOriginal].decode('utf-8')
        dt = datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
        return dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return None

def process_image(file, images_path):
    filename, ext = os.path.splitext(file)
    img_path = os.path.join(images_path, file)
    img = Image.open(img_path)
    
    # 初始化GPS信息为默认值
    gps_info = {"latitude": 0, "longitude": 0}
    timestamp = None
    
    # 尝试读取EXIF数据
    if 'exif' in img.info:
        exif_data = piexif.load(img.info['exif'])
        gps_info = get_gps_info(exif_data)
        timestamp = get_datetime_info(exif_data)

    # if not timestamp:
    #     timestamp = filename.split('_')[0]

    if file.endswith('_ahead.jpg'):
        data = {
            "filename": filename,
            "timestamp": timestamp,
            "gps": gps_info,
            "construction": -1,
            "road_damage": -1
        }
    elif file.endswith('_below.jpg'):
        data = {
            "filename": filename,
            "timestamp": timestamp,
            "gps": gps_info,
            "quantity": -1,
            "construction": -1,
            "road_damage": -1,
            "manhole": []
        }
    else:
        return

    json_filename = os.path.join(images_path, filename + '.json')
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, indent=2)

def main(images_path):
    for file in os.listdir(images_path):
        if file.endswith('.jpg'):
            process_image(file, images_path)

if __name__ == "__main__":
    images_path = 'jpg_init_test'  # 这里设置你想要处理的图片目录
    main(images_path)
