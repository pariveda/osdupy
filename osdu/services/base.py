class BaseService():

    def __init__(self, client, service_name: str, service_version: int):
        self._client = client
        self._service_url = f'{self._client.api_url}/api/{service_name}/v{service_version}'
