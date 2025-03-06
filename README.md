# prompt2txt

A tool for extracting Draw Things and Automatic1111 (A1111) prompts from PNG files and saving them as corresponding text files.

## Use Case

You have a large number of rendered PNG images created with Automatic1111 or Draw Things and need to extract the embedded prompts from them.

## Installation

### Using pip

```bash
pip install prompt2txt
```

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/prompt2txt.git
   cd prompt2txt
   ```

2. Install using Poetry:
   ```bash
   poetry install
   ```

## Usage

### Command Line

```bash
# Using the installed package
prompt2txt /path/to/image/folder/

# Using Poetry in the project directory
poetry run prompt2txt /path/to/image/folder/
```

### Python API

```python
from prompt2txt import PromptExtractor

extractor = PromptExtractor()
extractor.process_directory("/path/to/image/folder/")
```

## Features

- Extracts prompts from both Draw Things and Automatic1111 generated images
- Processes images in parallel for faster extraction
- Creates text files with the same name as the original PNG files
- Cleans and formats the extracted prompts

## Requirements

- Python 3.8+
- Dependencies (automatically installed):
  - Pillow
  - tqdm

## Caveats

- Automatic1111 may require enabling the "Save metadata to images" option to embed usable metadata.
- Some images may not contain extractable prompt data.

## Development

This project uses Poetry for dependency management and packaging:

```bash
# Install development dependencies
poetry install

# Run tests
poetry run pytest

# Build the package
poetry build
```

## License

[MIT License](LICENSE)
