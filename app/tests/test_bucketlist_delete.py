import json
import unittest

from test_setup import TestSetup


class TestBucketListDelete(TestSetup):

    def test_delete_inexistent_bucketlist(self):
        response = self.app.delete('/bucketlists/1',
                                   content_type='application/json',
                                   headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'bucketlist not found')

    def test_successful_bucketlist_deletion(self):
        bucketlist_data = {
            'name': 'Test Bucket List'
        }
        response = self.app.post('/bucketlists',
                                 data=json.dumps(bucketlist_data),
                                 content_type='application/json',
                                 headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'created bucketlist: {0}'.format(bucketlist_data['name']))
        # Delete the created Bucket List
        response = self.app.delete('/bucketlists/1',
                                   data=json.dumps(bucketlist_data),
                                   content_type='applicaiton/json',
                                   headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'successfully deleted bucketlist {0}'.format(1))


if __name__ == '__main__':
    unittest.main()
