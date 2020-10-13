from .base import BaseOsduClient


class SimpleOsduClient(BaseOsduClient):
    """BYOT: Bring your own token.
    
    This client assumes you are obtaining a token yourself (e.g. via your application's
    login form or otheer mechanism. With this SimpleOsduClient, you simply provide that token.
    With this simplicity, you are also then respnsible for reefreeshing the token as needed and
    re-instantiating the client with the new token.
    """
    
    def __init__(self, data_partition_id: str, access_token: str, api_url: str=None) -> None:
        """
        :param: access_token:   The access token only (not including the 'Bearer ' prefix).
        :param: api_url:        must be only the base URL, e.g. https://myapi.myregion.mydomain.com
        """
        super().__init__(data_partition_id, api_url)

        self._access_token = access_token