import os
import boto3

from .base import BaseOsduClient
import boto3.session


class AwsOsduClient(BaseOsduClient):
    """Good for batch tasks that don't have an interactive front-end. Token management is handled 
    with the boto3 library directly through the Cognito service. You have to supply additional arguments for this.

    Requires: `boto3`
    """

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, val):
        self._profile = val

    def __init__(self, data_partition_id, api_url:str=None, client_id:str=None, secret_hash:str=None,user:str=None, password:str=None, profile:str=None) -> None:
        """Authenticate and instantiate a new AWS OSDU client. Uses Cognito directly to obtain an access token.

        :param data_partition_id:   [Required] OSDU data partition ID, e.g. 'opendes'
        :param api_url:     Must be only the base URL, e.g. 'https://myapi.myregion.mydomain.com'
                            If not provided as arg, client will attempt to load value from 
                            environment variable: OSDU_API_URL.
        :param client_id:   OSDU client ID. Must be a Cognito App Client with no client secret.
        :param secret_hash: Amazon Cognito Secret hash. This is described here: 'https://aws.amazon.com/premiumsupport/knowledge-center/cognito-unable-to-verify-secret-hash/'
        :param user:        OSDU username. If not provided as arg, client will attempt to load value from
                            environment variable: OSDU_USER.
        :param password:    OSDU password. If not provided as arg, client will attempt to load value from
                            environment variable: OSDU_PASSWORD.
        :param profile:     Name of AWS profile to use for AWS session to retrieve tokens form Cognito. 
                            If not provided as arg, client will attempt to load value from 
                            environment variable: AWS_PROFILE.
        """
        super().__init__(data_partition_id, api_url)

        self._client_id = client_id or os.environ.get('OSDU_CLIENT_ID')
        self._user = user or os.environ.get('OSDU_USER')
        self._profile = profile or os.environ.get('AWS_PROFILE')
        self._secret_hash = secret_hash or os.environ.get('AWS_SECRETHASH')
        if password:
            self.get_tokens(password, secret_hash)
            password = None # Don't leave password lying around.
        else:
            self.get_tokens(os.environ.get('OSDU_PASSWORD'), secret_hash)

    def get_tokens(self, password, secret_hash) -> None:
        if self._profile:
            session = boto3.Session(profile_name=self._profile)
            print('Created boto3 session with profile: ', self._profile)
            cognito = session.client('cognito-idp')
        else:
            cognito = boto3.client('cognito-idp')

        auth_params = { 
            'USERNAME': self._user, 
            'PASSWORD': password
        }
        if secret_hash:
            auth_params['SECRET_HASH'] = secret_hash
        
        response = cognito.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=self._client_id,
            AuthParameters=auth_params
        )


        self._access_token = response['AuthenticationResult']['AccessToken']
        self._refresh_token = response['AuthenticationResult']['RefreshToken']
