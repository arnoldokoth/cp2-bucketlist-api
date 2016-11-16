import json
import unittest

from test_setup import TestSetup


class TestBucketListsPost(TestSetup):

    # Endpoint: /bucketlists -> POST
    def test_create_bucket_list_without_required_data(self):
        bucketlist_data = {}
        response = self.app.post('/bucketlists',
                                 content_type='application/json',
                                 headers=self.headers,
                                 data=json.dumps(bucketlist_data))
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'bucketlist name not provided')

    def test_create_duplicate_bucketlist_with_same_name(self):
        bucketlist_data = {
            'name': 'Learning Paths'
        }
        response = self.app.post('/bucketlists',
                                 data=json.dumps(bucketlist_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'created bucketlist: {0}'.format(bucketlist_data['name']))
        response = self.app.post('/bucketlists',
                                 data=json.dumps(bucketlist_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'bucketlist already exists')

    def test_successful_bucketlist_creation(self):
        bucketlist_data = {
            'name': 'Learning Paths'
        }
        response = self.app.post('/bucketlists',
                                 data=json.dumps(bucketlist_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'created bucketlist: {0}'.format(bucketlist_data['name']))

if __name__ == '__main__':
    unittest.main()
