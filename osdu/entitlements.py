""" Provides a simple Python interface to the OSDU Entitlements API.
"""
import requests
from .base import BaseService


class EntitlementsService(BaseService):

    def __init__(self, client):
        super().__init__(client, service_name='entitlements')
        self._service_url = f'{self._client.api_url}/Prod'

    def get_groups_for_user(self):
        """TODO"""
        url = f'{self._service_url}/groups'
        response = requests.get(url=url, headers=self._headers())
        response.raise_for_status()

        return response.json()