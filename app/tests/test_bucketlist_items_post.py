import json
import unittest

from test_setup import TestSetup


class TestBucketListItemPost(TestSetup):

    # Endpoint: /bucketlists/<int:bucketlist_id>/items -> POST
    def test_create_item_without_required_data(self):
        bucketlist_data = {
            'name': 'Test Bucket List'
        }
        response = self.app.post('/bucketlists',
                                 data=json.dumps(bucketlist_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'created bucketlist: {0}'.format(bucketlist_data['name']))

        item_data = {
            'name': ''
        }
        response = self.app.post('/bucketlists/1/items',
                                 data=json.dumps(item_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'please provide the name field')

    def test_duplicate_item_addition(self):
        bucketlist_data = {
            'name': 'Test Bucket List'
        }
        response = self.app.post('/bucketlists',
                                 data=json.dumps(bucketlist_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'created bucketlist: {0}'.format(bucketlist_data['name']))
        item_data = {
            'name': 'Test Bucket List Item'
        }
        response = self.app.post('/bucketlists/1/items',
                                 data=json.dumps(item_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'successfully added item {0}'.format(item_data['name']))
        response = self.app.post('/bucketlists/1/items',
                                 data=json.dumps(item_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'bucketlist item already exists')

    def test_successful_item_creation(self):
        bucketlist_data = {
            'name': 'Test Bucket List'
        }
        response = self.app.post('/bucketlists',
                                 data=json.dumps(bucketlist_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'created bucketlist: {0}'.format(bucketlist_data['name']))

        item_data = {
            'name': 'Test Bucket List Item'
        }
        response = self.app.post('/bucketlists/1/items',
                                 data=json.dumps(item_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'successfully added item {0}'.format(item_data['name']))


if __name__ == '__main__':
    unittest.main()
