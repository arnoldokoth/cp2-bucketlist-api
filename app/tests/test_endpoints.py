import json
import unittest

from datetime import datetime
from test_setup import TestSetup


class TestEndpoints(TestSetup):

    @unittest.skip("work in progress")
    def test_update_bucket_list(self):
        data = {
            'name': 'Updated Bucket List'
        }
        response = self.app.put('/bucketlists/1', data=data)
        self.assertEqual(response.status_code, 200)

    @unittest.skip("work in progress")
    def test_delete_bucket_list(self):
        # Try get the bucket list first with a get request
        # Assert that status_code 200 is returned
        response = self.app.delete('/bucketlists/1')
        self.assertEqual(response.status_code, 200)

    @unittest.skip("work in progress")
    def test_add_bucket_list_item(self):
        data = {
            'name': 'HTML Learning Path - Pluralsight',
            'date_created': datetime.utcnow,
            'date_modified': datetime.utcnow,
            'done': False
        }
        response = self.app.post('/bucketlists/1/items', data=data)
        self.assertEqual(response.status_code, 200)

    @unittest.skip("work in progress")
    def test_update_bucket_list_item(self):
        data = {
            'date_modified': datetime.utcnow,
            'done': True
        }
        response = self.app.put('/bucketlists/1/items/1', data=data)
        self.assertEqual(response.status_code, 200)

    @unittest.skip("work in progress")
    def test_delete_bucket_list_item(self):
        response = self.app.delete('/bucketlists/1/items/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
