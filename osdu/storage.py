""" Provides a simple Python interface to the OSDU Storage API.
"""
import requests
from .base import BaseService


class StorageService(BaseService):

    def __init__(self, client):
        super().__init__(client, service_name='storage')

    def get_record(self, record_id: str, data_partition_id=BaseService.DEFAULT_DATA_PARTITION):
        url = f'{self._service_url}/records/{record_id}'
        response = self.__execute_request('get', url, data_partition_id)

        return response.json()


    def query_all_kinds(self, data_partition_id=BaseService.DEFAULT_DATA_PARTITION):
        url = f'{self._service_url}/query/kinds'
        response = self.__execute_request('get', url, data_partition_id)

        return response.json()


    def store_records(self, records: list, data_partition_id=BaseService.DEFAULT_DATA_PARTITION):
        url = f'{self._service_url}/records'
        response = self.__execute_request('put', url, data_partition_id, json=records)

        return response.json()


    def delete_record(self, record_id: str, data_partition_id=BaseService.DEFAULT_DATA_PARTITION) -> bool:
        url = f'{self._service_url}/records/{record_id}'
        response = self.__execute_request('delete', url, data_partition_id)

        return response.status_code == 204


    def __execute_request(self, method:str, url: str, data_partition_id: str, json=None):
        headers = self._headers(data_partition_id)
        response = requests.request(method, url, headers=headers, json=json)
        if not response.ok:
            raise Exception(f'HTTP {response.status_code}', response.reason, response.text)

        return response
