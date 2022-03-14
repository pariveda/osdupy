""" Provides a simple Python interface to the OSDU Authentication API.
"""
import requests
from .base import BaseService
from time import time

class AuthenticationService(BaseService):

    def update_token(client):
        """Determines if the current access token associated with the client has expired.
        If the token is not expired, the current access_token will be returned, unchanged.
        If the token has expired, this function will attempt to refresh it, update it on client, and return it.
        For simple clients, refresh requires a OSDU_CLIENTWITHSECRET_ID, OSDU_CLIENTWITHSECRET_SECRET, REFRESH_TOKEN, and REFRESH_URL
        For Service Principal clients, refresh requires a resource_prefix and AWS_PROFILE (same as initial auth)
        For AWS clients, refresh requires OSDU_USER, OSDU_PASSWORD, AWS_PROFILE, and OSDU_CLIENT_ID
        
        :param client: client in use

        :returns: tuple containing 2 items: the new access token and it's expiration time
                        - access_token: used to access OSDU services
                        - expires_in:   expiration time for the token
        """
        if(AuthenticationService._need_update_token(client)):
            if (hasattr(client, "resource_prefix") and client.resource_prefix is not None): #service principal client
                token = AuthenticationService._update_token_service_principal(client)
            elif (hasattr(client, "profile") and client.profile is not None): #aws client
                token = AuthenticationService._update_token_aws(client)
            else: #simple client
                token = AuthenticationService._update_token_simple(client)
        else:
            token = client.access_token, client._token_expiration if hasattr(client, "_token_expiration") else None
        return token
    
    def _need_update_token(client):
        return hasattr(client, "_token_expiration") and client._token_expiration < time() or client.access_token is None

    
    def _update_token_simple(client) -> dict:
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
        client.update_token()
        return client._access_token, client._token_expiration

    def _auth_headers():
        return {
             "Content-Type": "application/x-www-form-urlencoded",
        }

    def get_headers(client):
        AuthenticationService.update_token(client)
        return {
            "Content-Type": "application/json",
            "data-partition-id": client._data_partition_id,
            "Authorization": "Bearer " + client.access_token
        }