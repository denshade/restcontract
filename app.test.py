import unittest
import os
import json
import tempfile
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True

    def tearDown(self):
        # Clean up any temporary files created during the tests
        for filename in os.listdir('data'):
            if filename.endswith('.json'):
                os.remove(os.path.join('data', filename))

    def test_upload_endpoint(self):
        response = self.app.post('/upload', json={'url': '/test', 'response': {'message': 'Test response'}})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        response = self.app.get('/test')
        self.assertEquals(response, {'message': 'Test response'})


    def test_get_endpoint_file_not_found(self):
        response = self.app.get('/get/nonexistent.json')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['error'], 'File not found.')


if __name__ == '__main__':
    unittest.main()
