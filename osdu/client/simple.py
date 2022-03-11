import os
from ._base import BaseOsduClient


class SimpleOsduClient(BaseOsduClient):
    """BYOT: Bring your own token.
    
    This client assumes you are obtaining a token yourself (e.g. via your application's
    login form or otheer mechanism. With this SimpleOsduClient, you simply provide that token.
    With this simplicity, you are also then respnsible for reefreeshing the token as needed either by manually
    re-instantiating the client with the new token or by providing the authentication client id, secret, refresh token, and refresh url. 
    """

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret
    
    @property
    def refresh_url(self):
        return self._refresh_url
    
    @property
    def refresh_token(self):
        return self._refresh_token

    @property
    def access_token(self):
        return self._access_token
    
    @access_token.setter
    def access_token(self, val):
        self._access_token = val

    
    def __init__(self, data_partition_id: str, access_token: str=None, api_url: str=None, refresh_token: str=None, refresh_url: str=None) -> None:
        """
        :param: access_token:   The access token only (not including the 'Bearer ' prefix).
        :param: api_url:        must be only the base URL, e.g. https://myapi.myregion.mydomain.com
        :param: refresh_token:   The refresh token only (not including the 'Bearer ' prefix).
        :param: refresh_url:   The authentication Url, typically a Cognito URL ending in "/token".
        """
        super().__init__(data_partition_id, api_url)

        self._access_token = access_token
        self._refresh_token = refresh_token or os.environ.get('OSDU_REFRESH_TOKEN')
        self._refresh_url = refresh_url or os.environ.get('OSDU_REFRESH_URL')
        self._client_id = os.environ.get('OSDU_CLIENTWITHSECRET_ID')
        self._client_secret = os.environ.get('OSDU_CLIENTWITHSECRET_SECRET')