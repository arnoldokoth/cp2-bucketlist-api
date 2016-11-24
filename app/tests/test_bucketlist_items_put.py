import json
import unittest

from test_setup import TestSetup


class TestBucketListItemPut(TestSetup):

    # Endpoint: /bucketlists/<int:bucketlist_id>/items/<int:item_id> -> PUT
    def test_update_item_with_invalid_data(self):
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
        item_data = {'done': None}
        response = self.app.put('/bucketlists/1/items/1',
                                data=json.dumps(item_data),
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'please provide the done field')

    @unittest.skip("WORK IN PROGRESS")
    def test_database_rejects_invalid_done_value(self):
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
        item_data = {'done': 'blahblah'}
        response = self.app.put('/bucketlists/1/items/1',
                                data=json.dumps(item_data),
                                content_type='application/json',
                                headers=self.headers)
        # import pdb; pdb.set_trace()
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'error updating bucket list item')

if __name__ == '__main__':
    unittest.main()
