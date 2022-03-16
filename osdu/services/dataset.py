""" Provides a simple Python interface to the OSDU Dataset API.
"""
from typing import List
import requests
from .base import BaseService


class DatasetService(BaseService):

    def __init__(self, client):
        super().__init__(client, service_name='dataset', service_version=1)

    def get_dataset_registry(self, registry_id: str):
        """ Get dataset registry object for the given dataset registry ID.

        :param registry_id:  Identifier for the dataset registry you wish to retrieve
        :returns:           The API Response
        """
        url = f'{self._service_url}/getDatasetRegistry?id={registry_id}'
        response = requests.get(url=url, headers=self._headers())
        response.raise_for_status()

        return response.json()

    def get_dataset_registries(self, registry_ids: List[str]):
        """ Get multiple dataset registry objects for the given list of dataset registry IDs.

        :param registry_ids:    List of identifiers for the dataset registry you wish to retrieve
        :returns:               The API Response
        """
        url = f'{self._service_url}/getDatasetRegistry?'
        data = {'datasetRegistryIds': registry_ids}
        response = requests.post(url=url, headers=self._headers(), json=data)
        response.raise_for_status()

        return response.json()

    def get_storage_instructions(self, kind_subtype: str):
        """ Get storage instructions for the given dataset type.

        :param kind_subtype:    Identifier for the dataset registry for which to retrieve source data
        :returns:               The API Response
        """
        url = f'{self._service_url}/getStorageInstructions?kindSubType={kind_subtype}'
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()

        return response.json()

    def register_dataset(self, datasetRegistries: List[dict]):
        """ Get storage instructions for the given dataset type.

        :param datasetRegistries:   List of dataset registry objects to register
        :returns:                   The API Response
        """
        url = f'{self._service_url}/registerDataset'
        response = requests.put(
            url, headers=self._headers(), json=datasetRegistries)
        response.raise_for_status()

        return response.json()

    def get_retrieval_instructions(self, dataset_registry_ids: List[dict]):
        """ Get instructions on how to retrieve a given dataset registry

        :param dataset_registry_ids:    Identifiers for the dataset registries for which to retrieve source data
        :returns:                       The API Response
        """
        url = f'{self._service_url}/getRetrievalInstructions'
        data = {'datasetRegistryIds': dataset_registry_ids}
        response = requests.post(
            url, headers=self._headers(), json=data)
        response.raise_for_status()

        return response.json()
