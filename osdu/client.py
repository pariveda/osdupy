""" Handles the authentication and token management for interacting with the OSDU platform.
"""

import os

import boto3

from osdu.delivery import DeliveryService
from osdu.search import SearchService
from osdu.storage import StorageService
from osdu.entitlements import EntitlementsService


class BaseOsduClient:

    @property
    def token(self):
        return self._token

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
    def entitlements(self):
        return self.__entitlements

    @property
    def delivery(self):
        return self._delivery

    @property
    def data_partition_id(self):
        return self._data_partition_id

    @data_partition_id.setter
    def data_partition_id(self, val):
        self._data_partition_id = val


    def __init__(self, data_partition_id, api_url:str=None, client_id:str=None, user:str=None, password:str=None):
        """Authenticate and instantiate a new OSDU client.
        
        'api_url' must be only the base URL, e.g. https://myapi.myregion.mydomain.com
        """
        # Environment variables.
        # TODO: Validate api_url against URL regex pattern.        
        self._api_url = (api_url or os.environ.get('OSDU_API_URL')).rstrip('/')
        self._client_id = client_id or os.environ.get('OSDU_CLIENT_ID')
        self._user = user or os.environ.get('OSDU_USER')
        p = password or os.environ.get('OSDU_PASSWORD')
        self._token = self.get_access_token(p)
        p = None # Don't leave password lying around.
        self._data_partition_id = data_partition_id

        # Instantiate services.
        self._search = SearchService(self)
        self._storage = StorageService(self)
        self._delivery = DeliveryService(self)
        self.__entitlements = EntitlementsService(self)

        # TODO: Implement these services.
        # self.__legal = LegaService(self)


    # Abstract Method
    def get_access_token(self, password):
        raise NotImplementedError('This method must be implemented by a subclass')


class AwsOsduClient(BaseOsduClient):

    def get_access_token(self, password):
        client = boto3.client('cognito-idp')
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=self._client_id,
            AuthParameters={ 'USERNAME': self._user, 'PASSWORD': password }
        )
        return "Bearer " + response['AuthenticationResult']['AccessToken']   
