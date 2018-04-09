# transcriber-segmentor
Python application to support segmentation of speech audio files.


## Example usage
### Transcribe an Alveo document URL
```bash
curl https://localhost:8080/api/segment/url?url=https://staging.alveo.edu.au/catalog/austalk/1_114_3_8_001/document/1_114_3_8_001-ch6-speaker16.wav
```

### Transcribe a generic URL
```bash
curl https://localhost:8080/api/segment/url?url=https://localhost:8080/test.wav
```

### Transcribe via a POST
```bash
curl -F "file=@test.wav" https://localhost:8080/api/segment/upload
```

## Deployment with Dokku

The application is deployed using dokku, the following configuration is required on the dokku host:

```bash
$ dokku app:create segmenter
$ dokku config:set segmenter ALVEO_API_KEY= <your API key> ALVEO_API_URL=http://app.alveo.edu.au/
```
Now you can push the repository to the dokku host using git:
```bash
$ git add remote dokku dokku@apps.alveo.edu.au:segmenter
$ git push dokku master
```
This should build the environment and start the application. We then need to set up an SSL certificate
on the dokku host:
```bash
$ dokku letsencrypt segmenter
```


