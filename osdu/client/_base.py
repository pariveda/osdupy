""" Handles the authentication and token management for interacting with the OSDU platform.
"""

import os
from time import time
from ..services.search import SearchService
from ..services.storage import StorageService
from ..services.dataset import DatasetService
from ..services.entitlements import EntitlementsService
from ..services.legal import LegalService


class BaseOsduClient:

    @property
    def access_token(self):
        self._ensure_valid_token()
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
    def entitlements(self):
        return self._entitlements

    @property
    def delivery(self):
        return self._delivery

    @property
    def dataset(self):
        return self._dataset
    
    @property
    def legal(self):
        return self.__legal

    @property
    def data_partition_id(self):
        return self._data_partition_id

    @data_partition_id.setter
    def data_partition_id(self, val):
        self._data_partition_id = val

    def __init__(self, data_partition_id, api_url: str = None):
        """Authenticate and instantiate a new OSDU client.

        'api_url' must be only the base URL, e.g. https://myapi.myregion.mydomain.com
        """
        self._data_partition_id = data_partition_id
        # TODO: Validate api_url against URL regex pattern.
        api_url = api_url or os.environ.get('OSDU_API_URL')
        if not api_url:
            raise Exception('No API URL found.')
        self._api_url = api_url.rstrip('/')

        # Instantiate services.
        self._search = SearchService(self)
        self._storage = StorageService(self)
        self._dataset = DatasetService(self)
        self._entitlements = EntitlementsService(self)
        self.__legal = LegalService(self)

    def _need_update_token(self):
        return hasattr(self, "_token_expiration") and self._token_expiration < time() or self._access_token is None

    def _ensure_valid_token(self):
        """Determines if the current access token associated with the client has expired.
        If the token is not expired, the current access_token will be returned, unchanged.
        If the token has expired, this function will attempt to refresh it, update it on client, and return it.
        For simple clients, refresh requires a OSDU_CLIENTWITHSECRET_ID, OSDU_CLIENTWITHSECRET_SECRET, REFRESH_TOKEN, and REFRESH_URL
        For Service Principal clients, refresh requires a resource_prefix and AWS_PROFILE (same as initial auth)
        For AWS clients, refresh requires OSDU_USER, OSDU_PASSWORD, AWS_PROFILE, and OSDU_CLIENT_ID
        
        :param client: client in use

        :returns: tuple containing 2 items: the new access token and it's expiration time
                        - access_token: used to access OSDU services
                        - expires_in:   expiration time for the token
        """
        if(self._need_update_token()):
            token = self._update_token()
        else:
            token = self._access_token, self._token_expiration if hasattr(self, "_token_expiration") else None
        return token

    def _update_token(self):
        pass #each client has their own update_token method
