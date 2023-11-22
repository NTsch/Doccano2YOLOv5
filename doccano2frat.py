import json
import os
import shutil
from PIL import Image
import random

# Define the path to your JSONL file
jsonl_file_path = "doccano.jsonl"

# Create a directory to store the output JSON files
output_directory = "frat"
shutil.rmtree(output_directory)
os.makedirs(output_directory)

# Open and iterate through the JSONL file
with open(jsonl_file_path, "r") as jsonl_file:
    for line in jsonl_file:
        try:
            # Parse each line as JSON
            data = json.loads(line)

            # Extract the "filename" key from the JSON
            filename = data.get("filename")

            if filename:
                # Create an empty JSON file with the extracted filename
                output_file_path = os.path.join(output_directory, f"{filename}.json")

                # Get the image file path from the "image" folder
                image_file_path = os.path.join("images", f"{filename}")

                # Check if the image file exists
                if os.path.isfile(image_file_path):
                    # Get the width and height of the image
                    with Image.open(image_file_path) as img:
                        width, height = img.size

                    content = {"image_wh": [width, height]}

                    # initiate empty lists
                    content["rect_LTRB"] = []
                    content["rect_classes"] = []
                    content["class_names"] = []
                    content["class_colors"] = []
                    content["user"] = ""
                    content["image_md5"] = filename.removesuffix('.jpg')

                    for bbox in data.get("bbox"):
                        content["rect_LTRB"].append(
                            [
                                round(bbox["x"]),
                                round(bbox["y"]),
                                round(bbox["x"] + bbox["width"]),
                                round(bbox["y"] + bbox["height"]),
                            ]
                        )
                        
                        # insert "class_names"
                        if bbox["label"] not in content["class_names"]: content["class_names"].append(bbox["label"])

                        # insert "rect_classes"
                        content["rect_classes"].append(content["class_names"].index(bbox["label"]))

                    # insert "class_colors" (optional?)
                    '''
                    for class_name in content["class_names"]:
                        r = lambda: random.randint(0,255)
                        hex_color = '#%02X%02X%02X' % (r(),r(),r())
                        content["class_colors"].append(hex_color)
                    '''

                    # Create an empty JSON file with the extracted filename
                    output_file_path = os.path.join(
                        output_directory, f"{filename}.json"
                    )
                    with open(output_file_path, "w") as output_file:
                        json.dump(content, output_file, indent=4)
                else:
                    print(f"No such image as {image_file_path}")

                print(f'Created JSON file: {output_file_path}')

            else:
                print('Skipping line - No "filename" key found.')

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

print("Finished creating JSON files.")
