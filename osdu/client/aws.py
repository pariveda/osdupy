import os
import boto3

from .base import BaseOsduClient


class AwsOsduClient(BaseOsduClient):
    """Good for batch tasks that don't have an interactive front-end. Token management is handled 
    with the boto3 library directly through the Cognito service. You have to supply additional arguments for this.

    Requires: `boto3`
    """

    def __init__(self, data_partition_id, api_url:str=None, client_id:str=None, user:str=None, password:str=None) -> None:
        super().__init__(data_partition_id, api_url)

        self._client_id = client_id or os.environ.get('OSDU_CLIENT_ID')
        self._user = user or os.environ.get('OSDU_USER')
        if password:
            self.get_tokens(password)
            password = None # Don't leave password lying around.
        else: 
            self.get_tokens(os.environ.get('OSDU_PASSWORD'))


    def get_tokens(self, password) -> None:
        client = boto3.client('cognito-idp')
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=self._client_id,
            AuthParameters={ 'USERNAME': self._user, 'PASSWORD': password }
        )

        self._access_token = response['AuthenticationResult']['AccessToken']
        self._refresh_token = response['AuthenticationResult']['RefreshToken']
