""" Provides a simple Python interface to the OSDU Delivery API.
"""
import requests
from .base import BaseService


class DeliveryService(BaseService):

    def __init__(self, client):
        super().__init__(client, service_name='delivery')

    def get_signed_urls(self, srns: [str], data_partition=BaseService.DEFAULT_DATA_PARTITION):
        url = f'{self._service_url}/GetFileSignedUrl'
        query = { 'srns': srns }
        response = requests.post(url=url, headers=self._headers(), json=query)
        if not response.ok:
            raise Exception(f'HTTP {response.status_code}', response.reason, response.text)

        return response.json()
