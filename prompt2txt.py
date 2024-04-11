# prompt2txt.py v0.2  Author: zanshinmu
# Extracts embedded prompts from Draw Things or Automatic1111 to a txt file for each image in the specified directory.
#
# Before running this script, ensure that exiftool is installed on your system.
# If you do not have exiftool installed, you can install it using Homebrew with the following command:
# 
#   brew install exiftool
# 
# This command installs exiftool, making it available for this script to use.
# Homebrew needs to be installed on your system to use the above command. If Homebrew is not installed,
# visit https://brew.sh/ for instructions on installing Homebrew.

import subprocess
import json
import os
import sys
import re
import glob
from tqdm import tqdm
from multiprocessing import Pool

def get_png_files(directory):
    png_files = glob.glob(os.path.join(directory, '*.png'))
    return png_files

def process_prompt_string(input_string):
    # Remove everything in "<>" using regular expression
    clean_string = re.sub(r'<.*?>', '', input_string)
    
    # Remove all instances of the string "BREAK"
    clean_string = clean_string.replace('BREAK', '')
    
    # Remove spaces, commas, and other leading characters
    clean_string = re.sub(r'^[,\s]+', '', clean_string)
    
    # Extract substring until '\n'
    index = clean_string.find('\n')
    if index != -1:
        result_string = clean_string[:index]
    else:
        result_string = clean_string
    
    return result_string
         
def extract_a1_prompt(parameters):
    # Parse the string in parameters
    comment_data = process_prompt_string(parameters)
    if not comment_data:
        print ("Error parsing prompt")
        return None
    else:
        return comment_data


def extract_dt_prompt(user_comment):
    try:
        # Parse the JSON string in the User Comment
        comment_data = json.loads(user_comment)
    except json.JSONDecodeError as e:
        print(f"Error parsing User Comment JSON: {e}")
        return None
    # Extract the prompt (associated with key 'c')
    return comment_data.get('c', '')
    
# We have to try both possible keynames
def get_a1_metadata(metadata):
    parameters = metadata.get('Parameters')
    if not parameters:
        parameters = metadata.get('parameters')
    if parameters:
        return parameters
    else:
        print ("No A1 Metadata found")
        return None

def process_file(filepath, metadata_list):
    metadata = metadata_list[0]
    if metadata:
        # Extract the 'User Comment' field
        user_comment = metadata.get('UserComment') # Ensure the key matches the actual metadata
        if user_comment:
            prompt = extract_dt_prompt(user_comment)
        else:
            parameters = get_a1_metadata(metadata)
            if parameters:
                prompt = extract_a1_prompt(parameters)
                if prompt == "":
                    print("A1 Prompt not found")
            else:
                print ("No metadata found")
                return False
        
        if prompt:
            # Write the prompt to a text file
            text_file_path = f"{os.path.splitext(filepath)[0]}.txt"
            with open(text_file_path, 'w') as text_file:
                text_file.write(prompt)
                text_file.close()
            return prompt
        else:
            print(f"No valid prompt metadata found for {filepath}.")
            return None
     
    else:
        print(f"No valid metadata found for {filepath}.")
        return None
        
def process_image(image_path):
    try:
        # Call exiftool with the JSON format option
        process = subprocess.run(['exiftool', '-json', image_path], capture_output=True, text=True)
        if process.returncode != 0:
            print(f"Error calling exiftool for {image_path}: {process.stderr}")
            return image_path, None
        # Parse the output as JSON
        metadata = json.loads(process.stdout)
        prompt = process_file(image_path, metadata)
        return image_path, prompt  # Assuming one file, return its metadata
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from exiftool output for {image_path}: {e}")
        return image_path, None

def pool_process_metadata(image_paths):
   
    with Pool() as pool:
        # Use tqdm to track progress
        results = list(tqdm(pool.imap(process_image, image_paths), total=len(image_paths), desc="Processing"))
    return {image_path: metadata for image_path, metadata in results}
    

# Walk the images
def main(directory):
    metadata = pool_process_metadata(get_png_files(directory))
    print(f"\n{len(metadata)} images processed.\n")
                

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    if os.path.isdir(directory):
        main(directory)
    else:
        print (f"{directory} not valid")
