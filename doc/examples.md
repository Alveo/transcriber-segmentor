### Document URL example
http://localhost:5000/api/segment/url?url=https://staging.alveo.edu.au/catalog/austalk/1_114_3_8_001/document/1_114_3_8_001-ch6-speaker16.wav

### Generic URL example
http://localhost:5000/api/segment/url?url=https://localhost:8080/test.wav

### Post example
curl -F "file=@test.wav" http://localhost:5000/api/segment/upload
