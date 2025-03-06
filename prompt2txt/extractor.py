import json
import os
import re
import glob
from tqdm import tqdm
from multiprocessing import Pool
from PIL import Image
import argparse

class PromptExtractor:
    def __init__(self):
        # Compiling regex here
        self.tag_regex = re.compile(r'<.*?>')
        self.broken_regex = re.compile(r'(^|\s)<\S*?[>\s]')
        self.spec_regex = re.compile(r'^[,\s]+')

    def get_png_files(self, directory):
        png_files = glob.glob(os.path.join(directory, '*.png'))
        return png_files

    def clean_prompt_string(self, input_string):
        # Remove everything in "<>" using regular expression
        clean_string = re.sub(self.tag_regex, '', input_string)
        
        # Remove broken tags
        clean_string = re.sub(self.broken_regex, '', clean_string)
        
        # Remove all instances of the string "BREAK"
        clean_string = clean_string.replace('BREAK', '')
        
        # Remove spaces, commas, and other leading characters
        clean_string = re.sub(self.spec_regex, '', clean_string)
        
        # Extract substring until '\n'
        index = clean_string.find('\n')
        if index != -1:
            result_string = clean_string[:index]
        else:
            result_string = clean_string
        
        return result_string
             
    def extract_a1_prompt(self, parameters):
        try:
            # For Pillow, parameters will be coming directly from img.info['parameters']
            # and needs to be decoded if it's bytes
            if isinstance(parameters, bytes):
                parameters = parameters.decode('utf-8')
            
            # Clean and parse the parameters string
            comment_data = self.clean_prompt_string(parameters)
            if not comment_data:
                print("Error parsing prompt")
                return None
            return comment_data
        except Exception as e:
            print(f"Error extracting A1111 prompt: {e}")
            return None

    def extract_dt_prompt(self, user_comment):
        try:
            # Parse the JSON string in the User Comment
            comment_data = json.loads(user_comment)
        except json.JSONDecodeError as e:
            print(f"Error parsing User Comment JSON: {e}")
            return None
        # Extract the prompt (associated with key 'c')
        return comment_data.get('c', '')

    def process_file(self, filepath, metadata):
        if 'usercomment' in metadata:
            prompt = self.extract_dt_prompt(metadata['usercomment'])
        elif 'parameters' in metadata:
            prompt = self.extract_a1_prompt(metadata['parameters'])
        else:
            print("No metadata found")
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
            
    def process_image(self, image_path):
        try:
            with Image.open(image_path) as img:
                metadata = {}
                
                # Check for Parameters field
                if 'parameters' in img.info:
                    metadata['parameters'] = img.info['parameters']
                    
                # Check for UserComment field in XMP
                xmp_data = img.info.get('XML:com.adobe.xmp', '')
                if xmp_data:
                    start = xmp_data.find('<rdf:li xml:lang="x-default">{"c"')
                    if start != -1:
                        end = xmp_data.find('</rdf:li>', start)
                        if end != -1:
                            json_str = xmp_data[start+29:end]
                            metadata['usercomment'] = json_str
                
                prompt = self.process_file(image_path, metadata)
                return image_path, prompt
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return image_path, None

    def pool_process_metadata(self, image_paths):
        with Pool() as pool:
            results = list(tqdm(pool.imap(self.process_image, image_paths),
                            total=len(image_paths),
                            desc="Processing"))
        return {image_path: metadata for image_path, metadata in results}

    def process_directory(self, directory):
        metadata = self.pool_process_metadata(self.get_png_files(directory))
        print(f"\n{len(metadata)} images processed.\n")
        return metadata

# Handle command line arguments if the file is run directly
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract prompts from AI generated images")
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help='Directory containing PNG files (default: current directory)')
    args = parser.parse_args()
    
    if os.path.isdir(args.directory):
        extractor = PromptExtractor()
        extractor.process_directory(args.directory)
    else:
        print(f"{args.directory} is not a valid directory")

