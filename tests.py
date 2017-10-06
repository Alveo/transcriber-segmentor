import unittest

from application import app

class Tester(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def testErrorPage(self):
        response = self.app.get('/clearlyshouldntexist')
        self.assertEqual(response.data, b'404') 

    def testDownloaderURL(self):
        attachments_invalid = [
                '?',
                '?url=',
                '?url=',
                '',
                '?url=http://localhost',
                '?url=http://localhost:5000',
                '?url=http://127.0.0.1',
                '?url=http://127.0.0.1:5000',
                '/file/',
        ]

        for attachment in attachments_invalid:
            response = self.app.get('/api/segment/url?url='+attachment)
            self.assertTrue(b'URL pattern is either not valid' in response.data)

        attachments_noconnect = [
                'http://somedomainthatdoesnexit/file',
                'http://somedomainthatdoesnexit.asdf/file',
                'http://127.168.8.55/file',
                'http://127.168.8.55:530/file',
                'http://somedomainthatdoesnexit:530/file',
        ]

        for attachment in attachments_noconnect:
            response = self.app.get('/api/segment/url?url='+attachment)
            self.assertTrue(b'Errno' in response.data)

# Block connections to self?

#http://localhost:5000/api/segment/url?url=https://staging.alveo.edu.au/catalog/austalk/1_114_3_8_001/document/1_114_3_8_001-ch6-speaker16.wav

### Generic URL
#http://localhost:5000/api/segment/url?url=https://localhost:8080/test.wav

### POST
#curl -F "file=@test.wav" http://localhost:5000/api/segment/upload

if __name__ == '__main__':
    unittest.main()
