from unittest import TestCase, mock

from osdu.client import AwsOsduClient


class TestOsduClient(TestCase):

    @mock.patch('boto3.client')
    def test_initialize_aws_client_with_args(self, mock_client):
        api_url = 'https://your.api.url.com'
        client_id = 'YOURCLIENTID'
        user = 'username@testing.com'
        password = 'p@ssw0rd'

        client = AwsOsduClient('opendes',
            api_url=api_url,  
            client_id=client_id,  
            user=user,  
            password=password)

        self.assertIsNotNone(client)
