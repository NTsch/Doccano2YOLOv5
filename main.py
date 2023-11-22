import json
import os
import shutil
from PIL import Image

# takes in a JSONL with Doccano annotations and converts them to YOLOv5 annotation format
# Doccano format: labels are saved with names, 1 .jsonl with 1 line per image - x & y coordinates of upper left corner, height, width, all as pixels
# YOLOv5 format: labels are saved as 0-indexed numbers, 1 .txt per image - x & y coordinates of center, height, width, all as ratios of image size

# TODO: make sure that all yolo annotation files reference the same labels.txt file

doccano_path = 'admin.jsonl'
yolov5_path = 'yolov5_noe_500'

# create the 'yolov5' directory for the outputs
if os.path.exists(yolov5_path):
    shutil.rmtree(yolov5_path)
    os.makedirs(yolov5_path)

# labels are saved in dict, this must correspond to YOLO .yaml
unique_labels_dict = {}

with open(doccano_path) as json_file:
    json_list = json_file.readlines()

    for json_str in json_list:
        json_obj = json.loads(json_str)
        img_name = json_obj['filename'].removesuffix('.jpg')

        img_path = os.path.join('images', img_name + '.jpg')  # adjust 'images_directory' as needed

        # add label names to dict
        for bbox in json_obj['bbox']:
            label = bbox['label']
            if label not in unique_labels_dict:
                unique_labels_dict[label] = len(unique_labels_dict)
        
            # open image to get its dimensions
            with Image.open(img_path) as img:
                img_width, img_height = img.size

            with open(f'{yolov5_path}/{img_name}.txt', 'a+') as yolo_file:
            
                # calculate ratios
                x_upper_left = bbox['x'] / img_width
                y_upper_left = bbox['y'] / img_height
                width = bbox['width'] / img_width
                height = bbox['height'] / img_height
                x_center = x_upper_left + (width / 2)
                y_center = y_upper_left + (height / 2)

                label_index = unique_labels_dict[label]

                # write YOLOv5 format annotation to file
                yolo_file.write(f"{label_index} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    # write YOLOv5 label file
    with open(f'{yolov5_path}/labels.txt', 'w') as label_file:
        for key in unique_labels_dict.keys():
            label_file.write(key + "\n")

print("Conversion to YOLOv5 format completed.")
