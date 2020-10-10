from typing import Pattern
from unittest import TestCase, mock

from osdu.client import AwsOsduClient, SimpleOsduClient


class TestAwsOsduClient(TestCase):

    @mock.patch('boto3.client')
    def test_initialize_aws_client_with_args(self, mock_client):
        partition = 'opendes'
        api_url = 'https://your.api.url.com'
        client_id = 'YOURCLIENTID'
        user = 'username@testing.com'
        password = 'p@ssw0rd'

        client = AwsOsduClient(partition,
            api_url=api_url,  
            client_id=client_id,  
            user=user,  
            password=password)

        self.assertIsNotNone(client)
        self.assertEqual(partition, client.data_partition_id)


class TestSimpleOsduClient(TestCase):

    def test_initialize_simple_client_with_token(self):
        partition = 'opendes'
        token = 'mytoken'

        client = SimpleOsduClient(partition, token)

        self.assertEqual(partition, client.data_partition_id)
        self.assertEqual(token, client.access_token)