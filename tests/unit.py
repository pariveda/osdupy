import base64
import hashlib
import hmac
from unittest import TestCase, mock
from time import time

from osdu.client import (
    AwsOsduClient,
    AwsServicePrincipalOsduClient,
    SimpleOsduClient
)


class TestAwsServicePrincipalOsduClient(TestCase):

    @mock.patch('osdu.client._service_principal_util.ServicePrincipalUtil.get_service_principal_token', return_value=["testtoken",time()+ 999])
    @mock.patch('boto3.Session')
    @mock.patch('base64.b64decode')
    def test_initialize_aws_client_with_args(self, mock_b64decode, mock_session, mock_sputil):
        partition = 'osdu'
        resource_prefix = 'r3mx'
        region = 'us-east-1'
        profile = 'myprofile'

        client = AwsServicePrincipalOsduClient(
            partition, resource_prefix, profile=profile, region=region)

        self.assertIsNotNone(client)
        self.assertEqual(partition, client.data_partition_id)
        self.assertIsNotNone(client.access_token)
        self.assertIsNotNone(client.api_url)


class TestAwsOsduClient(TestCase):

    @mock.patch('boto3.Session')
    def test_initialize_aws_client(self, mock_session):
        partition = 'opendes'
        api_url = 'https://your.api.url.com'
        client_id = 'YOURCLIENTID'
        user = 'username@testing.com'
        password = 'p@ssw0rd'
        profile = 'osdu-dev'

        client = AwsOsduClient(
            partition,
            api_url=api_url,
            client_id=client_id,
            user=user,
            password=password,
            profile=profile
        )

        self.assertIsNotNone(client)
        self.assertEqual(partition, client.data_partition_id)

    @mock.patch('boto3.Session')
    def test_initialize_aws_client_with_client_secret(self, mock_session):
        partition = 'opendes'
        api_url = 'https://your.api.url.com'
        client_id = 'YOURCLIENTID'
        client_secret = 'YOURCLIENTSECRET'
        user = 'username@testing.com'
        password = 'p@ssw0rd'
        profile = 'osdu-dev'

        message = user + client_id
        dig = hmac.new(
            client_secret.encode('UTF-8'), msg=message.encode('UTF-8'), digestmod=hashlib.sha256).digest()
        secret_hash = base64.b64encode(dig).decode()

        client = AwsOsduClient(
            partition,
            api_url=api_url,
            client_id=client_id,
            user=user,
            password=password,
            secret_hash=secret_hash,
            profile=profile
        )

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
