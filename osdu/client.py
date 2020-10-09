""" Handles the authentication and token management for interacting with the OSDU platform.
"""

import os

import boto3

from osdu.delivery import DeliveryService
from osdu.search import SearchService
from osdu.storage import StorageService


class BaseOsduClient:

    @property
    def access_token(self):
        return self._access_token

    @property
    def api_url(self):
        return self._api_url

    @property
    def search(self):
        return self._search

    @property
    def storage(self):
        return self._storage

    @property
    def delivery(self):
        return self._delivery

    @property
    def data_partition_id(self):
        return self._data_partition_id

    @data_partition_id.setter
    def data_partition_id(self, val):
        self._data_partition_id = val


    def __init__(self, data_partition_id, api_url:str=None):
        """Authenticate and instantiate a new OSDU client.
        
        'api_url' must be only the base URL, e.g. https://myapi.myregion.mydomain.com
        """
        self._data_partition_id = data_partition_id
        # TODO: Validate api_url against URL regex pattern.        
        self._api_url = (api_url or os.environ.get('OSDU_API_URL')).rstrip('/')

        # Instantiate services.
        self._search = SearchService(self)
        self._storage = StorageService(self)
        self._delivery = DeliveryService(self)
        # TODO: Implement these services.
        # self.__legal = LegaService(self)
        # self.__entitlements = EntitlementsService(self)

    # Abstract Method
    def get_tokens(self, password):
        raise NotImplementedError('This method must be implemented by a subclass')



class SimpleOsduClient(BaseOsduClient):
    """BYOT: Bring your own token.
    
    This client assumes you are obtaining a token yourself (e.g. via your application's
    login form or otheer mechanism. With this SimpleOsduClient, you simply provide that token.
    With this simplicity, you are also then respnsible for reefreeshing the token as needed and
    re-instantiating the client with the new token.
    """
    
    def __init__(self, data_partition_id: str, access_token: str, api_url: str=None) -> None:
        """
        :param: access_token:   The access token only (not including the 'Bearer ' prefix).
        :param: api_url:        must be only the base URL, e.g. https://myapi.myregion.mydomain.com
        """
        super().__init__(data_partition_id, api_url)

        self._access_token = access_token


class AwsOsduClient(BaseOsduClient):

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

