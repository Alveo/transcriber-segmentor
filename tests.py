import unittest

from application import app

class Tester(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

        self.url_pattern_fail = "URL pattern is either not valid"
        self.url_connection_fail = "Errno"

        self.attachments_generic_urls = [
                {
                    'expect': self.url_pattern_fail,
                    'items': [
                        '?',
                        '?url=',
                        '?url=',
                        '',
                        '?/file/'
                    ]
                },
                {
                    'expect': self.url_connection_fail,
                    'items': [
                        '?url=http://somedomainthatdoesnexit/file',
                        '?url=http://somedomainthatdoesnexit.asdf/file',
                        '?url=http://127.0.0.55/file',
                        '?url=http://127.0.0.55:530/file',
                        '?url=http://somedomainthatdoesnexit:530/file',
                    ]
                },
            ]

    def testErrorPage(self):
        response = self.app.get('/clearlyshouldntexist')
        self.assertEqual(response.data, b'404') 

        response = self.app.get('/api/segment/url/fail')
        self.assertEqual(response.data, b'404') 

    def testDownloaderURLGenericDisabled(self):
        app.config['ALLOW_GENERIC_URL'] = False
        for attachment in self.attachments_generic_urls:
            for item in attachment['items']:
                response = self.app.get('/api/segment/url'+item)
                self.assertTrue(self.url_pattern_fail in bytes.decode(response.data))

    def testDownloaderURLGeneric(self):
        app.config['ALLOW_GENERIC_URL'] = True

        for attachment in self.attachments_generic_urls:
            for item in attachment['items']:
                response = self.app.get('/api/segment/url'+item)
                self.assertTrue(attachment['expect'] in bytes.decode(response.data))



#http://localhost:5000/api/segment/url?url=https://staging.alveo.edu.au/catalog/austalk/1_114_3_8_001/document/1_114_3_8_001-ch6-speaker16.wav

### Generic URL
#http://localhost:5000/api/segment/url?url=https://localhost:8080/test.wav

### POST
#curl -F "file=@test.wav" http://localhost:5000/api/segment/upload

if __name__ == '__main__':
    unittest.main()
