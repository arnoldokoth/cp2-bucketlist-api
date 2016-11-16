import json
import unittest

from test_setup import TestSetup


class TestBucketListsGet(TestSetup):

    # Endpoint: /bucketlists -> GET
    def test_get_bucket_list_without_creation(self):
        response = self.app.get('/bucketlists',
                                content_type='application/json',
                                headers=self.headers)
        self.assertEqual(str(json.loads(response.get_data())['message']),
                         'no bucketlist found')

if __name__ == '__main__':
    unittest.main()
