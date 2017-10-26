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

## Setup (manual)
See Dockerfile for build instructions
