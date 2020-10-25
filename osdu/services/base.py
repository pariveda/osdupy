class BaseService():

    def __init__(self, client, service_name):
        self._client = client
        self._service_url = f'{self._client.api_url}/api/{service_name}/v2'
    
    def _headers(self):
        return {
            "Content-Type": "application/json",
            "data-partition-id": self._client._data_partition_id,
            "Authorization": "Bearer " + self._client.access_token
        }