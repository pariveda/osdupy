import unittest
from unittest import mock
import requests
import boto3

from osdu.client import AwsOsduClient


class TestOsduClient(unittest.TestCase):

    @mock.patch('boto3.client')
    def test_initialize_aws_client_with_args(self, mock_client):
        api_url = 'https://your.api.url.com'
        client_id = 'YOURCLIENTID'
        user = 'username@testing.com'
        password = 'p@ssw0rd'

        osdu = AwsOsduClient('opendes',
            api_url=api_url,  
            client_id=client_id,  
            user=user,  
            password=password)

        self.assertIsNotNone(osdu)