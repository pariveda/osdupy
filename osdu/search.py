""" Provides a simple Python interface to the OSDU Search API.
"""
import requests
from .base import BaseService


class SearchService(BaseService):

    def __init__(self, client):
        super().__init__(client, 'search')

    
    def query_with_cursor(self, query: dict, max_results=100, data_partition_id=BaseService.DEFAULT_DATA_PARTITION, results=[], cursor='initial'):
        """Recursively retrieves all records resulting from `query`. Cursor is used to page through
        results larger than the 100 record limit per call.
        Base case: cursor == None

        :param query Dict representation of JSON query payload for REST API call.
        """
        headers = {
            "Content-Type": "application/json",
            "data-partition-id": data_partition_id,
            "Authorization": self._client.token
        }
        url = f'{self._service_url}/query_with_cursor'

        # Add cursor to request body for subsequent requests.
        if cursor != "initial":
            query["cursor"] = cursor
        
        response = requests.post(url=url, headers=headers, json=query)
        if not response.ok:
            raise Exception(f'HTTP {response.status_code}', response.reason, response.text)

        cursor, _results, total_count  = response.json().values()
        results += _results

        if cursor != None and len(results) < max_results:
            results = self.query_with_cursor(query, results=results, cursor=cursor)
        
        return results[:max_results]


    def query(self):
        raise NotImplementedError('This method is not yet implemented.')