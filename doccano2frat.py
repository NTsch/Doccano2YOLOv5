import json
import os
from PIL import Image

# Define the path to your JSONL file
jsonl_file_path = 'doccano.jsonl'

# Create a directory to store the output JSON files if it doesn't exist
output_directory = 'frat'
os.makedirs(output_directory, exist_ok=True)

# Open and iterate through the JSONL file
with open(jsonl_file_path, 'r') as jsonl_file:
    for line in jsonl_file:
        try:
            # Parse each line as JSON
            data = json.loads(line)
            
            # Extract the "filename" key from the JSON
            filename = data.get('filename')
            
            if filename:
                # Create an empty JSON file with the extracted filename
                output_file_path = os.path.join(output_directory, f'{filename}.json')
                
                # Get the image file path from the "image" folder
                image_file_path = os.path.join('images', f'{filename}')
                
                # Check if the image file exists
                if os.path.isfile(image_file_path):
                    # Get the width and height of the image
                    with Image.open(image_file_path) as img:
                        width, height = img.size
                    
                    image_wh = {'image_wh': [width, height]}
                else:
                    image_wh = {'image_wh': None}
                    
                # Create an empty JSON file with the extracted filename and the "image_wh" key
                output_file_path = os.path.join(output_directory, f'{filename}.json')
                with open(output_file_path, 'w') as output_file:
                    json.dump(image_wh, output_file, indent=4)
                    
                print(f'Created JSON file with "image_wh" key: {output_file_path}')
                
            else:
                print('Skipping line - No "filename" key found.')

        except json.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')

print('Finished creating JSON files.')
