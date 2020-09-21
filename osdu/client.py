""" Handles the authentication and token management for interacting with the OSDU platform.
"""

import logging
import os

import boto3

from osdu.delivery import DeliveryService
from osdu.search import SearchService
from osdu.storage import StorageService


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
    def delivery(self):
        return self._delivery


    def __init__(self, api_url:str=None, client_id:str=None, user:str=None, password:str=None):

        # TODO: Validate api_url against URL regex pattern.        
        self._api_url = api_url or os.environ.get('OSDU_API_URL')
        self._client_id = client_id or os.environ.get('OSDU_CLIENT_ID')
        self._user = user or os.environ.get('OSDU_USER')
        p = password or os.environ.get('OSDU_PASSWORD')
        self._token = self.get_access_token(p)
        p = None # Don't leave password lying around.

        # Instantiate services.
        self._search = SearchService(self)
        self._storage = StorageService(self)
        self._delivery = DeliveryService(self)

        # TODO: Implement these services.
        # self.__legal = LegaService(self)
        # self.__entitlements = EntitlementsService(self)


    # Abstract Method
    def get_access_token(self, password):
        raise NotImplementedError('This method must be implemented by a subclass')


class AwsOsduClient(BaseOsduClient):

        def __init__(self, api_url:str=None, client_id:str=None, user:str=None, password:str=None):
            super().__init__(api_url, client_id, user, password)


        def get_access_token(self, password):
            client = boto3.client('cognito-idp')
            response = client.initiate_auth(
                AuthFlow='USER_PASSWORD_AUTH',
                ClientId=self._client_id,
                AuthParameters={ 'USERNAME': self._user, 'PASSWORD': password }
            )
            return "Bearer " + response['AuthenticationResult']['AccessToken']   
