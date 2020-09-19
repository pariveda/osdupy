""" Handles the authentication and token management for interacting with the OSDU platform.
"""

from getpass import getpass
from osdu.search import SearchService
from osdu.storage import StorageService
from osdu.delivery import DeliveryService
import boto3
import os



def get_client(api_url:str=None, client_id:str=None, user:str=None, password:str=None):
    return OsduClient(api_url, client_id, user, password)


class OsduClient:

    @property
    def token(self):
        return self.__token

    @property
    def api_url(self):
        return self.__api_url

    @property
    def search(self):
        return self.__search

    @property
    def storage(self):
        return self.__storage

    @property
    def delivery(self):
        return self.__delivery


    def __init__(self, api_url:str=None, client_id:str=None, user:str=None, password:str=None):
        # TODO: Validate api_url against URL regex pattern.        
        self.__api_url = api_url or os.environ.get('OSDU_API_URL')
        self.__client_id = client_id or os.environ.get('OSDU_CLIENT_ID')
        self.__user = user or os.environ.get('OSDU_USER')
        p = password or os.environ.get('OSDU_PASSWORD')
        self.__token = self.__get_bearer_token(p)
        p = None # Don't leave password lying around.

        # Instantiate services.
        self.__search = SearchService(self)
        self.__storage = StorageService(self)
        self.__delivery = DeliveryService(self)

        # TODO: Implement these services.
        # self.__legal = LegaService(self)
        # self.__entitlements = EntitlementsService(self)


    def __get_bearer_token(self, password):
        client = boto3.client('cognito-idp')

        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            ClientId=self.__client_id,
            AuthParameters={
                'USERNAME': self.__user,
                'PASSWORD': password
                }
        )

        return "Bearer " + response['AuthenticationResult']['AccessToken']
