""" Provides a simple Python interface to the OSDU Entitlements API.
"""
import json
import requests
from .base import BaseService


class EntitlementsService(BaseService):

    def __init__(self, client):
        super().__init__(client, 'entitlements', service_version=2)


    def get_groups(self) -> dict:
        """Retrieves all the groups for the user or service extracted from the OSDU Entitlements Service.

        :returns:       dict containing results
                        - desId: str:   User Id.
                        - groups:      list:   of records resutling from search query  
                        - memberEmail:   str:    User email address
        """
        
        url = f'{self._service_url}/groups'
        query = {}
        response = requests.get(url=url, headers=self._headers(), json=query)
        response.raise_for_status()
        return response.json()

    def get_group_members(self, groupEmail:str=None) -> dict:
        """Returns the members of an OSDU Group.

        :param groupEmail:   String representing the email adress of the group to be listed.
    
        :returns:       dict members containing list of group members: 
                        - email: str:   Email Address of user
                        - roles: str:   OWNER or MEMBER         
        """
        
        url = f'{self._service_url}/groups/' + groupEmail + '/members'
        query = ''
        response = requests.get(url=url, headers=self._headers(), json=query)
        response.raise_for_status()
        return response.json()

    def add_group_member(self, groupEmail:str, query: dict) -> dict:
        """Adds a member to an OSDU Group.

        :param query:   dict representing the JSON-style query to be sent to the entitlements API. Must adhere to
                        the syntax suported by OSDU. For more details, see: 
                        https://community.opengroup.org/osdu/documentation/-/blob/master/platform/tutorials/core-services/EntitlementsService.md

        :returns:       dict query that was input           
        """
        
        url = f'{self._service_url}/groups/' + groupEmail + '/members'
        response = requests.post(url=url, headers=self._headers(), json=query)
        response.raise_for_status()
        return response.json()
                
    def delete_group_member(self, groupEmail:str, query: dict) -> dict:
        """Deletes a member from an OSDU Group.

        :param query:   dict representing the JSON-style query to be sent to the entitlements API. Must adhere to
                        the syntax suported by OSDU. For more details, see: 
                        https://community.opengroup.org/osdu/documentation/-/blob/master/platform/tutorials/core-services/EntitlementsService.md

        :returns:       dict query that was input
        """
        
        url = f'{self._service_url}/groups/' + groupEmail + '/members'
        response = requests.delete(url=url, headers=self._headers(), json=query)
        response.raise_for_status()
        return response.json()


    def create_group(self, groupEmail:str, query: dict) -> dict:
        """Create an OSDU Group

        :param query:   dict representing the JSON-style query to be sent to the entitlements API. Must adhere to
                        the syntax suported by OSDU. For more details, see: 
                        https://community.opengroup.org/osdu/documentation/-/blob/master/platform/tutorials/core-services/EntitlementsService.md

        :returns:       dict containing members: aggregations, results, totalCount
                        - aggregations: dict:   returned only if 'aggregateBy' specified in query
                        - results:      list:   of records resutling from search query  
                        - totalCount:   int:    the total number of results despite any 'limit' specified in the
                                                query or the 1,000 record limit of the API
        """
        
        url = f'{self._service_url}/groups/' + groupEmail + '/members'
        response = requests.delete(url=url, headers=self._headers(), json=query)
        response.raise_for_status()
        return response.json()