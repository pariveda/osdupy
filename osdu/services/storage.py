""" Provides a simple Python interface to the OSDU Storage API.
"""
from typing import List
import requests
from .base import BaseService
from .authentication import AuthenticationService


class StorageService(BaseService):

    def __init__(self, client):
        super().__init__(client, service_name='storage', service_version=2)

    def get_record(self, record_id: str):
        """Returns the latest version of the given record."""
        url = f'{self._service_url}/records/{record_id}'
        response = self.__execute_request('get', url)

        return response.json()

    def get_records(self, record_ids: List[str], attributes: List[str] = []):
        """Fetches multiple records at once.

        :param record_ids:  List of record ids. Each record id must follow the naming convention {OSDU-Account-Id}:{dataset-name}:{record-type}:{version}.
                            example: tenant1:well:123456789
        :param attributes:  Filter attributes to restrict the returned fields of the record. Usage: data.{record-data-field-name}.
                            example: data.wellName
        """
        url = f'{self._service_url}/query/records'
        payload = {'records': record_ids, 'attributes': attributes}
        response = self.__execute_request('post', url, json=payload)

        return response.json()

    def query_all_kinds(self):
        """Returns a list of all kinds in the current data partition."""
        url = f'{self._service_url}/query/kinds'
        response = self.__execute_request('get', url)

        return response.json()

    def store_records(self, records: list):
        """Create and/or update records. When no record id is provided or when the provided id is not already present 
        in the Data Ecosystem, then a new record is created. If the id is related to an existing record in the Data 
        Ecosystemthen an update operation takes place and a new version of the record is created.

        """
        url = f'{self._service_url}/records'
        response = self.__execute_request('put', url, json=records)

        return response.json()

    def delete_record(self, record_id: str) -> bool:
        """Performs a logical deletion of the given record. This operation can be reverted later.
        
        :returns:   True if record deleted successfully. Otherwise False.
        """
        url = f'{self._service_url}/records/{record_id}:delete'
        response = self.__execute_request('post', url)

        return response.status_code == 204

    def purge_record(self, record_id: str) -> bool:
        """performs the physical deletion of the given record and all of its versions. This operation cannot be undone.
        
        :returns:   True if record was purged successfully. Otherwise False.
        """
        url = f'{self._service_url}/records/{record_id}'
        response = self.__execute_request('delete', url)

        return response.status_code == 204

    def get_all_record_versions(self, record_id: str):
        """Returns a list containing all versions for the given record id."""
        url = f'{self._service_url}/records/versions/{record_id}'
        response = self.__execute_request('get', url)

        return response.json()

    def get_record_version(self, record_id: str, version: str):
        """Retrieves the specific version of the given record."""
        url = f'{self._service_url}/records/{record_id}/{version}'
        response = self.__execute_request('get', url)

        return response.json()

    def __execute_request(self, method: str, url: str, json=None):
        headers = AuthenticationService.get_headers(self._client)
        response = requests.request(method, url, headers=headers, json=json)
        response.raise_for_status()

        return response
