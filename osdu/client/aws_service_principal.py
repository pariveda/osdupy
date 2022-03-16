from ._base import BaseOsduClient
from ._service_principal_util import ServicePrincipalUtil


class AwsServicePrincipalOsduClient(BaseOsduClient):

    @property
    def resource_prefix(self):
        return self._resource_prefix

    def __init__(self, data_partition_id: str, resource_prefix: str, profile: str = None, region: str = None):
        self._sp_util = ServicePrincipalUtil(
            resource_prefix, profile=profile, region=region)
        self._resource_prefix = resource_prefix
        token_and_expiration = self._get_tokens()
        self._access_token = token_and_expiration[0]
        self._token_expiration = token_and_expiration[1]

        super().__init__(data_partition_id, self._sp_util.api_url)

    def _get_tokens(self):
        return self._sp_util.get_service_principal_token(self._resource_prefix)
   
    def _update_token(self):
        self._access_token, self._token_expiration = self._sp_util.get_service_principal_token(self._resource_prefix)
        return self._access_token, self._token_expiration
