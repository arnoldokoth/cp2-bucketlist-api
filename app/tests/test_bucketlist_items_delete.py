import json
import unittest

from test_setup import TestSetup


class TestBucketListItemDelete(TestSetup):

    # Endpoint: /bucketlists/<int:bucketlist_id>/items/<int:item_id> -> DELETE
    def test_delete_from_inexistent_bucketlist(self):
        response = self.app.delete('/bucketlists/1/items/1',
                                   content_type='application/json',
                                   headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                        'bucketlist not found')

    def test_delete_inexistent_item(self):
        bucketlist_data = {
            'name': 'Test Bucket List'
        }
        response = self.app.post('/bucketlists',
                                 data=json.dumps(bucketlist_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'created bucketlist: {0}'.format(bucketlist_data['name']))
        response = self.app.delete('/bucketlists/1/items/1',
                                   content_type='application/json',
                                   headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                        'bucketlist item does not exist')

    def test_successful_item_deletion(self):
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
        response = self.app.delete('/bucketlists/1/items/1',
                                   content_type='application/json',
                                   headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                        'successfully deleted bucketlist item')


if __name__ == '__main__':
    unittest.main()
