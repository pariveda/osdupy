from unittest import TestCase, mock

from osdu.client.aws import AwsOsduClient
from osdu.client.simple import SimpleOsduClient

import hmac
import hashlib
import base64


class TestAwsOsduClient(TestCase):

    @mock.patch('boto3.Session')
    def test_initialize_aws_client_with_args(self, mock_session):
        partition = 'opendes'
        api_url = 'https://your.api.url.com'
        client_id = 'YOURCLIENTID'
        client_secret = 'YOURCLIENTSECRET'
        user = 'username@testing.com'
        password = 'p@ssw0rd'
        profile = 'osdu-dev'



        message = user + client_id
        dig = hmac.new(client_secret.encode('UTF-8'), msg=message.encode('UTF-8'),digestmod=hashlib.sha256).digest()
        secretHash = base64.b64encode(dig).decode()



        client = AwsOsduClient(partition,
                               api_url=api_url,
                               client_id=client_id,
                               user=user,
                               password=password,
                               profile=profile)

        self.assertIsNotNone(client)
        self.assertEqual(partition, client.data_partition_id)


class TestSimpleOsduClient(TestCase):

    def test_initialize_simple_client_with_token(self):
        partition = 'opendes'
        token = 'mytoken'
        api_url = 'https://your.api.url.com'

        client = SimpleOsduClient(partition, token, api_url=api_url)

        self.assertEqual(partition, client.data_partition_id)
        self.assertEqual(token, client.access_token)
