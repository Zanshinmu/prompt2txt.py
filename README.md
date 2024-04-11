# prompt2txt.py
## Extracts Draw Things and A1111 prompts to txt files corresponding to PNG files in a specified directory
___
Use case: You have a large number of rendered png images in a directory created with A1111 or Draw Things which you need to extract the prompts from. 
___

## DualModel *experimental*
Two-model processing, Llava 1.5 and Mixtral. Mixtral is running on Ollama, Llava on LLama C++ Python
Mixtral parses the prompt and queries LLava for each element then Mixtral constructs a caption from the responses.
Why Ollama?  Two instances of Llama C++ python do not work.  Ollama works fine even though it has a llama c++ back-end.
DualModel is being released as experimental: it is slow and has a tendency to go off-course over time,
but that may be fixable with grammar and optimizations. 

# Installation Guide

This guide provides instructions for setting up the necessary requirements for `prompt2txt.py`


## Setting Up Python Virtual Environment and Installing Dependencies

This repository utilizes Python 3 and relies on specific dependencies to function properly. To ensure a consistent environment and manage these dependencies efficiently, it's recommended to set up a Python virtual environment. This isolates the project's dependencies from other Python projects on your system.

### Setting Up a Python Virtual Environment

1. **Install Python 3**: If you haven't already, [download and install Python 3](https://www.python.org/downloads/) for your operating system.

2. **Install `virtualenv` (if not already installed)**: `virtualenv` is a tool used to create isolated Python environments. If you haven't installed it yet, you can do so via pip, Python's package installer. Run the following command in your terminal:

    ```
    pip install virtualenv
    ```

3. **Create a Virtual Environment**: Navigate to your project directory in the terminal and create a new virtual environment by running:

    ```
    python3 -m venv venv
    ```

    This command will create a folder named `venv` in your project directory, containing the Python interpreter and standard library for your virtual environment.

4. **Activate the Virtual Environment**: Before you can install dependencies or run your project within the virtual environment, you need to activate it. On macOS/Linux, run:

    ```
    source venv/bin/activate
    ```

    On Windows, run:

    ```
    venv\Scripts\activate
    ```

    Once activated, you should see `(venv)` prefixed to your terminal prompt, indicating that you are now working within the virtual environment.

### Installing Dependencies

This project uses a `requirements.txt` file to specify its dependencies. To install these dependencies, ensure that your virtual environment is activated, and then run:

```
pip install -r requirements.txt
```

This command will install all the required dependencies listed in the `requirements.txt` file.

### Deactivating the Virtual Environment

Once you're done working on your project, you can deactivate the virtual environment by simply running:

```
deactivate
```

This will return you to your system's default Python environment.

By following these steps, you'll have a clean, isolated environment for your Python project, with all the necessary dependencies installed.


# Caveats

- A1111 may require enabling the embedded metadata feature to produce usable metadata. 

## Usage

The `prompt2txt.py` script can be used as follows:

- Process a directory of images into prompt files:
  ```bash
  python3 prompt2txt.py /path/to/image/folder/
  ```
