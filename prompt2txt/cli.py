import argparse
import os
import sys
from .extractor import PromptExtractor

def main():
    parser = argparse.ArgumentParser(description="Extract prompts from AI generated images")
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
                        help='Directory containing PNG files (default: current directory)')
    args = parser.parse_args()
    
    if os.path.isdir(args.directory):
        extractor = PromptExtractor()
        extractor.process_directory(args.directory)
    else:
        print(f"{args.directory} is not a valid directory")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
