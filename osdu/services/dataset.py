""" Provides a simple Python interface to the OSDU Dataset API.
"""
import requests
from .base import BaseService


class DatasetService(BaseService):

    def __init__(self, client):
        super().__init__(client, service_name='dataset', service_version=1)

    def get_signed_urls(self, srns: list):
        """Given a list of SRNs representing files, return the signed URLs for those files."""
        url = f'{self._service_url}/GetFileSignedUrl'
        query = {'srns': srns}
        response = requests.post(url=url, headers=self._headers(), json=query)
        response.raise_for_status()

        return response.json()

    def get_dataset_registry(self, registry_id):
        """ Get dataset registry object for the given dataset registry ID

        :param registry_id:  Identifier for the dataset registry you wish to retrieve
        :returns:           The API Response
        """
        url = f'{self._service_url}/getDatasetRegistry?id={registry_id}'
        response = requests.post(url=url, headers=self._headers())
        response.raise_for_status()

        return response.json()

    def get_storage_instructions(self, kind_subtype):
        """ Get dataset registry object for the given dataset registry ID

        :param kind_subtype:    ...
        :returns:               The API Response
        """
        url = f'{self._service_url}/getStorageInstructions?kindSubType={kind_subtype}'
        response = requests.get(url=url, headers=self._headers())
        response.raise_for_status()

        return response.json()

    def register_dataset(self, datasetRegistries):
        url = f'{self._service_url}/registerDataset'
        response = requests.put(
            url=url, headers=self._headers(), json=datasetRegistries)
        response.raise_for_status()

        return response.json()
