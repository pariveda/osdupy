""" Provides a simple Python interface to the OSDU Storage API.
"""
import requests
from .base import BaseService


class StorageService(BaseService):

    def __init__(self, client):
        super().__init__(client, service_name='storage')

    def get_record(self, record_id: str, data_partition_id=BaseService.DEFAULT_DATA_PARTITION):
        url = f'{self._service_url}/records/{record_id}'
       
        return self.__execute_request(url, data_partition_id)


    def query_all_kinds(self, data_partition_id=BaseService.DEFAULT_DATA_PARTITION):
        url = f'{self._service_url}/query/kinds'

        return self.__execute_request(url, data_partition_id)['results']


    def store_record(self, record: list, data_partition_id=BaseService.DEFAULT_DATA_PARTITION):
        url = f'{self._service_url}/records'
        headers = self.__headers(data_partition_id)
        response = requests.put(url=url, headers=headers, json=record)
        if not response.ok:
            raise Exception(f'HTTP {response.status_code}', response.reason, response.text)

        return response.json()


    def delete_record(self, record_id: str, data_partition_id=BaseService.DEFAULT_DATA_PARTITION) -> bool:
        url = f'{self._service_url}/records/{record_id}'
        headers = self.__headers(data_partition_id)
        response = requests.delete(url=url, headers=headers)
        if not response.ok:
            raise Exception(f'HTTP {response.status_code}', response.reason, response.text)

        return response.status_code == 204


    def __execute_request(self, url: str, data_partition_id: str):
        headers = self.__headers(data_partition_id)
        response = requests.get(url=url, headers=headers)
        if not response.ok:
            raise Exception(f'HTTP {response.status_code}', response.reason, response.text)

        return response.json()

    
    def __headers(self, data_partition_id):
        return {
            "Content-Type": "application/json",
            "data-partition-id": data_partition_id,
            "Authorization": self._client.token
        }