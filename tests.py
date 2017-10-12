import unittest

from application import app

from flask import Flask

class Tester(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

        self.url_pattern_fail = "URL pattern is either not valid"
        self.url_connection_fail = "Errno"

        self.attachments_generic_urls_good = [
                {
                    'expect': None,
                    'items': [
                        '?url=http://127.0.0.1:5001/static/test.wav',
                        '?url=http://127.0.0.1:5001/static/depth/test.wav',
                    ]
                },
            ]

        self.attachments_generic_urls_file_invalid = [
                {
                    'expect': None,
                    'items': [
                        '?url=http://127.0.0.1:5001/notvalid',
                        '?url=http://127.0.0.1:5001/depth/notvalid',
                    ]
                },
            ]

        self.attachments_generic_urls_bad = [
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
                        '?url=http://127.0.0.55:530/api/segment/upload',
                        '?url=http://127.0.0.55:530/api/segment/url',
                        '?url=http://somedomainthatdoesnexit:530/file',
                    ]
                },
            ]

    def testErrorPage(self):
        response = self.app.get('/clearlyshouldntexist')
        self.assertEqual(response.data, b'404') 

        response = self.app.get('/api/segment/url/fail')
        self.assertEqual(response.data, b'404') 

    def testPostFileDisabled(self):
        app.config['ALLOW_POST_FILE'] = False
        response = self.app.post('/api/segment/upload')
        self.assertEqual(response.data, b'404') 

    def testDownloaderURLGenericDisabledFail(self):
        app.config['ALLOW_GENERIC_URL'] = False

        for attachment in self.attachments_generic_urls_bad:
            for item in attachment['items']:
                response = self.app.get('/api/segment/url'+item)
                self.assertTrue(self.url_pattern_fail in bytes.decode(response.data))

    def testDownloaderURLGenericFail(self):
        app.config['ALLOW_GENERIC_URL'] = True

        for attachment in self.attachments_generic_urls_bad:
            for item in attachment['items']:
                response = self.app.get('/api/segment/url'+item)
                self.assertTrue(attachment['expect'] in bytes.decode(response.data))

    def testDownloaderURLGenericFileInvalid(self):
        app.config['ALLOW_GENERIC_URL'] = True

        for attachment in self.attachments_generic_urls_file_invalid:
            for item in attachment['items']:
                response = self.app.get('/api/segment/url'+item)
                self.assertTrue(attachment['expect'] in bytes.decode(response.data))

    def testValidGeneric(self):
        app.config['ALLOW_GENERIC_URL'] = True

        # Set up tmp Flask environment with test/ as static_dir
        testenv = Flask(__name__, port=5001, static_dir='/test')

        for attachment in self.attachments_generic_urls_good:
            for item in attachment['items']:
                response = self.app.get('/api/segment/url'+item)
                self.assertTrue(attachment['expect'] in bytes.decode(response.data))

        # Close testenv

    #def testValidAlveo(self):
    #    # Set up tmp Flask environment with test/ as static_dir
    #    testenv = Flask(__name__, port=5001, static_dir='/test')

    #    for attachment in self.attachments_generic_urls_alveo:
    #        for item in attachment['items']:
    #            response = self.app.get('/api/segment/url'+item)
    #            self.assertTrue(attachment['expect'] in bytes.decode(response.data))

    #    # Close testenv



#http://localhost:5000/api/segment/url?url=https://staging.alveo.edu.au/catalog/austalk/1_114_3_8_001/document/1_114_3_8_001-ch6-speaker16.wav

### Generic URL
#http://localhost:5000/api/segment/url?url=https://localhost:8080/test.wav

### POST
#curl -F "file=@test.wav" http://localhost:5000/api/segment/upload

if __name__ == '__main__':
    unittest.main()
