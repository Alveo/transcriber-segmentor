# transcriber-segmentor
Python application to support segmentation of audio files for alveo-transcriber.

## Config (docker-compose)
1. `cp docker-compose.override-example.yml docker-compose.override.yml`
2. See SSL below, else remove `web:` section from `docker-compose.override.yml`

### SSL
1. `mkdir ./ssl`
2. `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./ssl/ssl.key -out ./ssl/ssl.crt`
3. `openssl dhparam -out ./ssl/dhparam.pem 2048`
4. edit `docker-compose.override.yml`, 

### Alveo API
Edit `docker-compose.override.yml`, put your Alveo API key in here

## Setup (docker-compose)
1. Install docker, docker-compose
2. docker-compose build
3. docker-compose up -d

## Setup (Manual)
1. Install Audioseg (see https://github.com/Alveo/docker-audioseg)
  - Recommended: Set up a python3 virtual environment

2. Install dependencies
  - pip install -r requirements.txt

3. Run the Flask application
  - python run.py

## Important
Use of the Alveo service requires an API key to be configured. From PyAlveo documents:
>You also need to download your API key (alveo.config) from the Alveo web application (click on your email address at the top right) and save it in your home directory
>- Linux or Unix: /home/<user>
>- Mac: /Users/<user>
>- Windows: C:\\Users\\<user>
