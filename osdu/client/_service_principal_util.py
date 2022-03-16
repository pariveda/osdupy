# Copyright © 2020 Amazon Web Services
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# ===================================
# REVISIONS
# ===================================
#
# Date          Author & Description
# ---------     ---------------------
# 2022-02-23    mike.duffy@parivedasolutions.com
#               - Updated constructor to optionally accept AWS profile and region instead of
#                 a boto3 session.
#               - Constructor to require resource_prefix and make this an instance variable.
#               - Refactored _get_secret method to fix UnboundLocalError for local variable 'secret'.
#               - Refactored _get_secret method to simplify try/except flow and to print secret_name on exception.
#               - Updated formatting to be PEP8-compliant.
#
import base64
from time import time
import boto3
import requests
import json
import botocore.exceptions


class ServicePrincipalUtil:

    @property
    def api_url(self):
        return self._api_url

    def __init__(
            self,
            resource_prefix: str,
            aws_session: boto3.Session = None,
            region: str = None,
            profile: str = None
    ):
        """If a session is not provided, then region and profile must be provided. 
        If none of these are provided, then boto3.Session will check for env vars: AWS_PROFILE and AWS_DEFAULT_REGION. 
        If not found there, then instantiation will fail.

        :param resource_prefix: Resource prefix from OSDU deployment. e.g. 'osdur3mX'
        :param aws_session: boto3 sesssion to use for retrieving paramaeters an secrets for the OSDU instance.
        :param region:  AWS Region where OSDU instance is deployed. e.g. 'us-east-1'
        :param profile: AWS credentials (CLI) profile name.
        """
        # If a boto session is provided, then use it. Otherwise, instantiate a new one with provided
        # region and profile.
        if aws_session:
            self._session = aws_session
        else:
            self._session = boto3.Session(
                region_name=region, profile_name=profile)
        self._api_url = self._get_ssm_parameter(
            f'/osdu/{resource_prefix}/api/url')

    def _get_ssm_parameter(self, ssm_path):
        ssm_client = self._session.client('ssm')
        ssm_response = ssm_client.get_parameter(Name=ssm_path)
        return ssm_response['Parameter']['Value']

    def _get_secret(self, secret_name, secret_dict_key):
        client = self._session.client(service_name='secretsmanager')
        # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        try:
            secret_response = client.get_secret_value(SecretId=secret_name)
            secret_val = None
            if 'SecretString' in secret_response:
                secret_val = secret_response['SecretString']
            elif 'SecretBinary' in secret_response:
                secret_val = base64.b64decode(secret_response['SecretBinary'])
            secret_json = json.loads(secret_val)[secret_dict_key]
            return secret_json
        except botocore.exceptions.ClientError as e:
            print(
                f"Could not get client secret '{secret_name}' from secrets manager")
            raise e

    def get_service_principal_token(self, resource_prefix):

        token_url_ssm_path = f'/osdu/{resource_prefix}/oauth-token-uri'
        aws_oauth_custom_scope_ssm_path = f'/osdu/{resource_prefix}/oauth-custom-scope'
        client_id_ssm_path = f'/osdu/{resource_prefix}/client-credentials-client-id'
        client_secret_name = f'/osdu/{resource_prefix}/client_credentials_secret'
        client_secret_dict_key = 'client_credentials_client_secret'

        client_id = self._get_ssm_parameter(client_id_ssm_path)
        client_secret = self._get_secret(
            client_secret_name, client_secret_dict_key)
        token_url = self._get_ssm_parameter(token_url_ssm_path)
        aws_oauth_custom_scope = self._get_ssm_parameter(
            aws_oauth_custom_scope_ssm_path)

        auth = '{}:{}'.format(client_id, client_secret)
        encoded_auth = base64.b64encode(str.encode(auth))

        headers = {}
        headers['Authorization'] = 'Basic ' + encoded_auth.decode()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        token_url = '{}?grant_type=client_credentials&client_id={}&scope={}'.format(
            token_url, client_id, aws_oauth_custom_scope)

        response = requests.post(url=token_url, headers=headers)
        response_json = json.loads(response.content.decode())
        return response_json['access_token'], response_json['expires_in'] + time()
