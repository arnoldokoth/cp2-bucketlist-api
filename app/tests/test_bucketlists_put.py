import json
import unittest

from test_setup import TestSetup


class TestBucketListPut(TestSetup):

    def test_update_bucket_list_without_name(self):
        bucketlist_data = {
            'name': 'Test Bucket List'
        }
        self.app.post('/bucketlists',
                      content_type='application/json',
                      headers=self.headers,
                      data=json.dumps(bucketlist_data))
        bucketlist_data = {'name': ''}
        response = self.app.put('/bucketlists/1',
                                content_type='application/json',
                                headers=self.headers,
                                data=json.dumps(bucketlist_data))
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'please provide a name')

    def test_update_bucket_list_with_name(self):
        bucketlist_data = {
            'name': 'Test Bucket List'
        }
        response = self.app.post('/bucketlists',
                                 content_type='application/json',
                                 headers=self.headers,
                                 data=json.dumps(bucketlist_data))
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'created bucketlist: {0}'.format(bucketlist_data['name']))
        bucketlist_data = {'name': 'Test Bucket List  Update'}
        response = self.app.put('/bucketlists/1',
                                content_type='application/json',
                                headers=self.headers,
                                data=json.dumps(bucketlist_data))
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'bucketlist {0} updated successfully'.format(1))

if __name__ == '__main__':
    unittest.main()
