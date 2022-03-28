""" Provides a simple Python interface to the OSDU Legal API.
"""
from typing import List
import requests
from .base import BaseService


class LegalService(BaseService):

    def __init__(self, client):
        super().__init__(client, service_name='legal', service_version=1)

    def get_legaltag(self, legaltag_name: str):
        """Returns information about the given legaltag."""
        url = f'{self._service_url}/legaltags/{legaltag_name}'
        response = self.__execute_request('get', url)

        return response.json()
    
    def create_legaltag(self, legaltag: dict):
        """Create a new legaltag. """
        url = f'{self._service_url}/legaltags'
        response = self.__execute_request('post', url, json=legaltag)

        return response.json()
    
    def delete_legaltag(self, legaltag_id: str) -> bool:
        """Deletes the given legaltag. This operation cannot be reverted (except by re-creating the legaltag).
        
        :returns:   True if legaltag deleted successfully. Otherwise False.
        """
        url = f'{self._service_url}/legaltags/{legaltag_id}'
        response = self.__execute_request('delete', url)

        return response.status_code == 204

    def get_legaltags(self, isValid: bool = True):
        """Fetches all matching legaltags.

        :param valid:  Boolean to restrict results to only valid legaltags (true) or only invalid legal tags (false). Default is true
        """
        url = f'{self._service_url}/legaltags/' + ('?valid=true' if isValid else '?valid=false')
        response = self.__execute_request('get', url)

        return response.json()

    def update_legaltag(self, legaltag: dict):
        """Updates a legaltag. Empty properties are ignored, not deleted.

        :param legaltag:  dictionary of properties to add/change to an existing legaltag
        """
        url = f'{self._service_url}/legaltags'
        response = self.__execute_request('put', url, json=legaltag)

        return response.json()

    def batch_retrive_legaltags(self, legaltag_names: List[str]):
        """Retrieves information about a list of legaltags
        
        :param legaltag_names:  List of legaltag names to fetch information about
        """
        url = f'{self._service_url}/legaltags:batchRetrieve'
        payload = {'names': legaltag_names}
        response = self.__execute_request('post', url, json=payload)

        return response.json()

    def validate_legaltags(self, legaltag_names: List[str]):
        """Validates the given legaltags--returning a list of which legaltags are invalid.
        
        :param legaltag_names:  List of legaltag names to validate
        """
        url = f'{self._service_url}/legaltags:validate'
        payload = {'names': legaltag_names}
        response = self.__execute_request('post', url, json=payload)

        return response.json()

    def get_legaltag_properties(self):
        """Fetch information about possible valuesn for legaltag properties"""
        url = f'{self._service_url}/legaltags:properties'
        response = self.__execute_request('get', url)

        return response.json()

    def __execute_request(self, method: str, url: str, json=None):
        headers = self._headers()
        response = requests.request(method, url, headers=headers, json=json)
        response.raise_for_status()

        return response
