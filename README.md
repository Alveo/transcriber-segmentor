# transcriber-segmentor
Python application to support segmentation of audio files for alveo-transcriber.

# Requirements
- Audioseg

# Setup 
1. Recommended: Set up a python3 virtual environment

2. Install Flask dependencies
  - pip install -r requirements.txt

3. Set up database fixtures
  - python manage.py gendb sample

4. Run the Flask application
  - python manage.py runserver
