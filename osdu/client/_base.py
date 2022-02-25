""" Handles the authentication and token management for interacting with the OSDU platform.
"""

import os

from ..services.search import SearchService
from ..services.storage import StorageService
from ..services.dataset import DatasetService
from ..services.entitlements import EntitlementsService


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
    def entitlements(self):
        return self._entitlements

    @property
    def delivery(self):
        return self._delivery

    @property
    def dataset(self):
        return self._dataset

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
        # TODO: Implement these services.
        # self.__legal = LegaService(self)

