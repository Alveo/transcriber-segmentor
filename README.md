# transcriber-segmentor
Python application to support segmentation of audio files for alveo-transcriber.

# Requirements
- Audioseg

# Setup 
1. Recommended: Set up a python3 virtual environment

2. Install Flask dependencies
  - pip install -r requirements.txt

3. Run the Flask application
  - python run.py

# Important
Use of the Alveo service requires an API key to be configured. From PyAlveo documents:
>You also need to download your API key (alveo.config) from the Alveo web application (click on your email address at the top right) and save it in your home directory
>- Linux or Unix: /home/<user>
>- Mac: /Users/<user>
>- Windows: C:\\Users\\<user>
