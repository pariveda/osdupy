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


    def __init__(self, data_partition_id, api_url:str=None, client_id:str=None, user:str=None, password:str=None, profile:str=None) -> None:
        """Authenticate and instantiate a new AWS OSDU client. Uses Cognito directly to obtain an access token.
        
        :param data_partition_id:   [Required] OSDU data partition ID, e.g. 'opendes'
        :param api_url:     Must be only the base URL, e.g. 'https://myapi.myregion.mydomain.com'
                            If not provided as arg, client will attempt to load value from 
                            environment variable: OSDU_API_URL.
        :param client_id:   OSDU client ID. Must be a Cognito App Client with no client secret.
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
        if password:
            self.get_tokens(password)
            password = None # Don't leave password lying around.
        else: 
            self.get_tokens(os.environ.get('OSDU_PASSWORD'))


    def get_tokens(self, password) -> None:
        if self._profile:
            session = boto3.Session(profile_name=self._profile)
            cognito = session.client('cognito-idp')
        else:
            cognito = boto3.client('cognito-idp')

        response = cognito.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=self._client_id,
            AuthParameters={ 'USERNAME': self._user, 'PASSWORD': password }
        )

        self._access_token = response['AuthenticationResult']['AccessToken']
        self._refresh_token = response['AuthenticationResult']['RefreshToken']
