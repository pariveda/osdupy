""" In order to run these tests, you must provide an appropriate `user` and `password`. The password
can be set locally by setting the environment variable OSDU_PASSWORD. If using
VS Code, then you can set this in your local `.env` file in your workspace directory to easily
switch between OSDU environments.
"""
from unittest import TestCase
from dotenv import load_dotenv

import requests
from osdu.client.aws import AwsOsduClient
from osdu.client.simple import SimpleOsduClient


load_dotenv(verbose=True)

data_partition = 'osdu'

class TestSimpleOsduClient(TestCase):
    
    def test_endpoint_access(self):
        # token = os.environ.get('OSDU_ACCESS_TOKEN')
        token = AwsOsduClient(data_partition).access_token
        query = {
            "kind": f"*:*:*:*",
            "limit": 1
        }
        client = SimpleOsduClient(data_partition, token)

        result = client.search.query(query)['results']

        self.assertEqual(1, len(result))


class TestAwsOsduClient(TestCase):

    def test_get_access_token(self):
        client = AwsOsduClient(data_partition)
        self.assertIsNotNone(client.access_token)


class TestOsduServiceBase(TestCase):

    @classmethod
    def setUpClass(cls):
        # Authenticate once for the test fixture.
        cls.osdu = AwsOsduClient(data_partition)
    

class TestSearchService_Query(TestOsduServiceBase):

    def test_simple_search_for_10_items(self): 
        query = {
            "kind": f"*:*:*:*",
            "limit": 10
        }
        result = self.osdu.search.query(query)['results']

        self.assertEqual(10, len(result))


    def test_get_all_wells(self):
        query_get_all_wells = {
            "kind": "*:*:master-data--Well:*",
        }

        result = self.osdu.search.query(query_get_all_wells)['results']

        # All results should be wells.
        wells = filter(lambda x : x['type'] == 'master-data--Well', result)

        self.assertCountEqual(wells, result)


    def test_get_all_wellbores(self):
        query = {
            "kind": "*:*:master-data--Wellbore:*",
        }

        result = self.osdu.search.query(query)['results']

        # All results should be well bores.
        wellbores = filter(lambda x : x['type'] == 'master-data--Wellbore', result)

        self.assertCountEqual(wellbores, result)


    def test_malformed_query_raises_exception(self):
        # Query with 3-part kind. Must be full 4-part kind.
        query = {
            "kind": "*:*:*"
        }
        with self.assertRaises(requests.HTTPError):
            should_fail = self.osdu.search.query(query)


class TestSearchService_QueryWithPaging(TestOsduServiceBase):

    def test_basic_paging(self):
        page_size = 100
        max_pages = 10
        query = {
            "kind": f"*:*:*:*",
            "limit": page_size
        }
        result = self.osdu.search.query_with_paging(query)

        # Iterate over first 'max_pages' pages and check that each page contains 'page_size' results.
        page_count = 1
        for page, total_count in result:
            with (self.subTest(i=page_count)):
                self.assertEqual(page_size, len(page), f'Failed on page #{page_count}')
            page_count += 1
            if page_count >= max_pages:
                break
        
        self.assertGreater(page_count, 1)


    def test_paging_gets_all_results(self):
        page_size = 1000
        query = {
            'kind': '*:*:master-data--Well:*',
            'limit': page_size
        }
        result = self.osdu.search.query_with_paging(query)

        record_count = 0
        total_count = 0
        for page, total in result:
            total_count = total
            record_count += len(page)
        
        self.assertGreater(record_count, 0)
        self.assertGreater(total_count, 0)
        self.assertEqual(total_count, record_count)

class TestStorageService(TestOsduServiceBase):

    def test_get_record(self):
        record_id_query = {
            "kind": "*:*:*:*",
            "limit": 1,
            "returnedFields": ["id"]
        }
        record_id = self.osdu.search.query(record_id_query)['results'][0]['id']

        result = self.osdu.storage.get_record(record_id)

        self.assertEqual(record_id, result['id'])


    def test_get_nonexistant_record_raises_excpetion(self):
        fake_record_id = 'opendes:doc:7be4fc7918e348c2bbc4d6f25b2ff334' #'ABC123'
        with self.assertRaises(requests.HTTPError):
            should_fail = self.osdu.storage.get_record(fake_record_id)


    def test_get_all_record_versions(self):
        record_id_query = {
            "kind": "*:*:master-data--Well:*",
            "limit": 1,
            "returnedFields": ["id"]
        }
        record_id = self.osdu.search.query(record_id_query)['results'][0]['id']

        result = self.osdu.storage.get_all_record_versions(record_id)

        self.assertEqual(record_id, result['recordId'])
        self.assertGreaterEqual(len(result['versions']), 1)


    def test_get_record_version(self):
        record_id_query = {
            "kind": "*:*:master-data--Well:*",
            "limit": 1
        }
        expected_record = self.osdu.search.query(record_id_query)['results'][0]

        result = self.osdu.storage.get_record_version(expected_record['id'], expected_record['version'])

        self.assertEqual(expected_record['id'], result['id'])
        self.assertEqual(expected_record['version'], result['version'])

