# transcriber-segmentor
Python application to support segmentation of audio files for alveo-transcriber.

## Config
1. See docker-compose.yml.dist
2. If you plan to use the Alveo API, it is recommended that you set the `ALVEO_API_KEY` environment variable accordingly

## Setup
### SSL
1. `mkdir ./ssl`
2. `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ./ssl/ssl.key -out ./ssl/ssl.crt`
3. `openssl dhparam -out ./ssl/dhparam.pem 2048`

### docker-compose
1. Install docker, docker-compose
2. Ensure a docker-compose.yml file is configured
3. Consider editing `config`
4. `docker-compose build`
5. `docker-compose up -d`

## Example usage
### Transcribe an Alveo document URL
`https://localhost:8080/api/segment/url?url=https://staging.alveo.edu.au/catalog/austalk/1_114_3_8_001/document/1_114_3_8_001-ch6-speaker16.wav`

### Transcribe a generic URL
`https://localhost:8080/api/segment/url?url=https://localhost:8080/test.wav`

### Transcribe via a POST
`curl -F "file=@test.wav" https://localhost:8080/api/segment/upload`
