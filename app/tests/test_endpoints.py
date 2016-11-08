from datetime import datetime
from test_setup import TestSetup


class TestEndpoints(TestSetup):

    @unittest.skip("work in progress")
    def test_user_registration(self):
        pass

    def test_user_login(self):
        credentials = {'username': 'arnoldokoth', 'password': 'somepassword'}
        response = self.app.post('/auth/login/', data=credentials)
        self.assertEqual(response.status_code, 200)

    def test_get_bucket_lists(self):
        response = self.app.get('/bucketlists')
        self.assertEqual(response.status_code, 200)

    def test_get_specific_bucket_list(self):
        response = self.app.get('/bucketlists/1')
        self.assertEqual(response.status_code, 200)

    def test_create_bucket_list(self):
        data = {
            'name': 'Learning Paths',
            'items': [
                {
                    'name': 'HTML Learning Path',
                }
            ],
            'created_by': 12294090
        }
        response = self.app.post('/bucketlists', data=data)
        self.assertEqual(response.status_code, 200)

    def test_update_bucket_list(self):
        data = {
            'name': 'Updated Bucket List'
        }
        response = self.app.put('/bucketlists/1', data=data)
        self.assertEqual(response.status_code, 200)

    def test_delete_bucket_list(self):
        # Try get the bucket list first with a get request
        # Assert that status_code 200 is returned
        response = self.app.delete('/bucketlists/1')
        self.assertEqual(response.status_code, 200)

    def test_add_bucket_list_item(self):
        data = {
            'name': 'HTML Learning Path - Pluralsight',
            'date_created': datetime.utcnow,
            'date_modified': datetime.utcnow,
            'done': False
        }
        response = self.app.post('/bucketlists/1/items', data=data)
        self.assertEqual(response.status_code, 200)

    def test_update_bucket_list_item(self):
        data = {
            'date_modified': datetime.utcnow,
            'done': True
        }
        response = self.app.put('/bucketlists/1/items/1', data=data)
        self.assertEqual(response.status_code, 200)

    def test_delete_bucket_list_item(self):
        response = self.app.delete('/bucketlists/1/items/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
