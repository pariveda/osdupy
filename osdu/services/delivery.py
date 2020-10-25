""" Provides a simple Python interface to the OSDU Delivery API.
"""
import requests
from .base import BaseService


class DeliveryService(BaseService):

    def __init__(self, client):
        super().__init__(client, service_name='delivery')

    def get_signed_urls(self, srns: list):
        """Given a list of SRNs representing files, return the signed URLs for those files."""
        url = f'{self._service_url}/GetFileSignedUrl'
        query = { 'srns': srns }
        response = requests.post(url=url, headers=self._headers(), json=query)
        response.raise_for_status()

        return response.json()
