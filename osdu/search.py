""" Provides a simple Python interface to the OSDU Search API.
"""
import requests
from .base import BaseService
import logging


class SearchService(BaseService):

    def __init__(self, client):
        super().__init__(client, 'search')


    def query(self, query: dict) -> dict:
        """

        :param query:   dict representing the JSON-style query to be sent to the search API. Must adhere to
                        the Lucene syntax suported by OSDU. For more details, see: 
                        https://community.opengroup.org/osdu/documentation/-/wikis/Releases/R2.0/OSDU-Query-Syntax

        :returns:       dict containing 3 items: aggregations, results, totalCount
                        - aggregations: dict:   returned only if 'aggregateBy' specified in query
                        - results:      list:   of records resutling from search query  
                        - totalCount:   int:    the total number of results despite any 'limit' specified in the
                                                query or the 1,000 record limit of the API
        """
        url = f'{self._service_url}/query'
        response = requests.post(url=url, headers=self._headers(), json=query)
        if not response.ok:
            raise Exception(f'HTTP {response.status_code}', response.reason, response.text)

        return response.json()


    def query_with_paging(self, query: dict):
        url = f'{self._service_url}/query_with_cursor'
        cursor='initial'

        try:
            while cursor:
                # Add cursor to request body for subsequent requests.
                if cursor != "initial":
                    query["cursor"] = cursor
                
                response = requests.post(url=url, headers=self._headers(), json=query)
                response.raise_for_status()

                cursor, results, total_count  = response.json().values()
                yield results, total_count

        except requests.exceptions.HTTPError as e:
            logging.error(e)
            raise e
