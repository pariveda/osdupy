""" Provides a simple Python interface to the OSDU Authentication API.
"""
import requests
from .base import BaseService
from time import time

class AuthenticationService(BaseService):

    def update_token(client):
        if(AuthenticationService._need_update_token(client)):
            if (hasattr(client, "resource_prefix") and client.resource_prefix is not None): #service principal client
                token = AuthenticationService._update_token_service_principal(client)
            elif (hasattr(client, "profile") and client.profile is not None): #aws client
                token = AuthenticationService._update_token_aws(client)
            else: #simple client
                token = AuthenticationService._update_token_simple(client)
        else:
            token = client.access_token, client._token_expiration
        return token
    
    def _need_update_token(client):
        return hasattr(client, "_token_expiration") and client._token_expiration < time() or client.access_token is None

    
    #TODO add expiration time to return
    def _update_token_simple(client) -> dict:
        """Executes a query against the OSDU search service.

        :param client:   the simple client being used. In order to refresh the token, the client must have:
                            client_id: corresponding to the clientwithsecret
                            client_secret: corresponding to the clientwithsecret
                            refresh_token
                            refresh_url
                         all are set via optional parameters in the SimpleClient constructor or environment variables

        :returns:       tuple containing 2 items: the access_token and it's expiration_time
                        - access_token: used to access OSDU services
                        - expires_in:   expiration time for the token
        """
        data = {'grant_type': 'refresh_token',
                'client_id': client.client_id,
                'client_secret': client.client_secret,
                'refresh_token': client.refresh_token,
                'scope': 'openid email'}
        response = requests.post(url=client.refresh_url,headers=AuthenticationService._auth_headers(), data=data)
        response.raise_for_status()

        return response.json()["access_token"],response.json()["expires_in"] + time()
    
    def _update_token_aws(client) -> dict:
        client.update_token()
        return client._access_token, client._token_expiration
    
    def _update_token_service_principal(client) -> dict:
        return client.update_token()

    def _auth_headers():
        return {
             "Content-Type": "application/x-www-form-urlencoded",
             "Accept-Encoding": "gzip, deflate, br"
        }