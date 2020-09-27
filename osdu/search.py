""" Provides a simple Python interface to the OSDU Search API.
"""
import requests
from .base import BaseService
import logging


class SearchService(BaseService):

    def __init__(self, client):
        super().__init__(client, 'search')


    def query(self, query: dict) -> dict:
        """Executes a query against the OSDU search service.

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
        """Executes a query with cursor against the OSDU search service. Returns a generator, which can than be
        iterated over to retrieve each page in the result set without having to deal with any cursor.

        :param query:   dict representing the JSON-style query to be sent to the search API. Must adhere to
                        the Lucene syntax suported by OSDU. For more details, see: 
                        https://community.opengroup.org/osdu/documentation/-/wikis/Releases/R2.0/OSDU-Query-Syntax

        :returns:       iterator of tuple containing 2 items: (results, totalCount)
                        - results:      list:   one page of records resutling from search query. Default page size
                                                is 10. This can be modified by passing the 'limit' parameter in
                                                query with the maximum allowed being 1000.
                        - totalCount:   int:    the total number of results despite any 'limit' specified in the
                                                query or the 1,000 record limit of the API
        """
        url = f'{self._service_url}/query_with_cursor'
        cursor=''

        try:
            while cursor:
                # Add cursor to request body for subsequent requests.
                if cursor != '':
                    query['cursor'] = cursor
                
                response = requests.post(url=url, headers=self._headers(), json=query)
                response.raise_for_status()

                cursor, results, total_count  = response.json().values()
                if not cursor:  # Effetive do-while condition
                    break
                else:
                    yield results, total_count

        except requests.exceptions.HTTPError as e:
            logging.error(e)
            raise e
