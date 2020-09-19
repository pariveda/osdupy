class BaseService():

    DEFAULT_DATA_PARTITION='opendes'

    def __init__(self, client, service_name=None):
        self._client = client
        self._service_url = f'{self._client.api_url}/api/{service_name}/v2'
    
    def _headers(self, data_partition_id=DEFAULT_DATA_PARTITION):
        return {
            "Content-Type": "application/json",
            "data-partition-id": data_partition_id,
            "Authorization": self._client.token
        }