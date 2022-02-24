""" In order to run these tests, you must provide an appropriate `user` and `password`. The password
can be set locally by setting the environment variable OSDU_PASSWORD. If using
VS Code, then you can set this in your local `.env` file in your workspace directory to easily
switch between OSDU environments.
"""
import json
import os
from unittest import TestCase

import requests
from dotenv import load_dotenv
from osdu.client import (
    AwsOsduClient,
    AwsServicePrincipalOsduClient,
    SimpleOsduClient
)

load_dotenv(verbose=True, override=True)

data_partition = 'osdu'


class TestSimpleOsduClient(TestCase):

    def test_endpoint_access(self):
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


class TestAwsServicePrincipalOsduClient(TestCase):

    def test_get_access_token(self):
        client = AwsServicePrincipalOsduClient(
            data_partition,
            os.environ['OSDU_RESOURCE_PREFIX'],
            profile=os.environ['AWS_PROFILE'],
            region=os.environ['AWS_DEFAULT_REGION']
        )
        self.assertIsNotNone(client.access_token)
        self.assertIsNotNone(client.api_url)

    def test_endpoint_access(self):
        query = {
            "kind": f"*:*:*:*",
            "limit": 1
        }
        client = AwsServicePrincipalOsduClient(
            data_partition,
            os.environ['OSDU_RESOURCE_PREFIX'],
            profile=os.environ['AWS_PROFILE'],
            region=os.environ['AWS_DEFAULT_REGION']
        )

        result = client.search.query(query)['results']

        self.assertEqual(1, len(result))


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
        wells = filter(lambda x: x['type'] == 'master-data--Well', result)

        self.assertCountEqual(wells, result)

    def test_get_all_wellbores(self):
        query = {
            "kind": "*:*:master-data--Wellbore:*",
        }

        result = self.osdu.search.query(query)['results']

        # All results should be well bores.
        wellbores = filter(lambda x: x['type'] ==
                           'master-data--Wellbore', result)

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
                self.assertEqual(page_size, len(
                    page), f'Failed on page #{page_count}')
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

    def test_get_records(self):
        record_id_query = {
            "kind": "*:*:*:*",
            "limit": 10,
            "returnedFields": ["id"]
        }
        results = self.osdu.search.query(record_id_query)['results']
        ids = list(map(lambda x: x['id'], results))

        response = self.osdu.storage.get_records(ids)
        actual_ids = list(map(lambda x: x['id'], response['records']))

        self.assertEqual(set(actual_ids), set(ids))

    def test_get_nonexistant_record_raises_excpetion(self):
        fake_record_id = 'opendes:doc:7be4fc7918e348c2bbc4d6f25b2ff334'  # 'ABC123'
        with self.assertRaises(requests.HTTPError):
            should_fail = self.osdu.storage.get_record(fake_record_id)

    def test_get_all_record_versions(self):
        record_id_query = {
            "kind": "*:*:*:*",
            "limit": 1,
            "returnedFields": ["id"]
        }
        record_id = self.osdu.search.query(record_id_query)['results'][0]['id']

        result = self.osdu.storage.get_all_record_versions(record_id)

        self.assertEqual(record_id, result['recordId'])
        self.assertGreaterEqual(len(result['versions']), 1)

    def test_get_record_version(self):
        record_id_query = {
            "kind": "*:*:*:*",
            "limit": 1
        }
        expected_record = self.osdu.search.query(record_id_query)['results'][0]

        result = self.osdu.storage.get_record_version(
            expected_record['id'], expected_record['version'])

        self.assertEqual(expected_record['id'], result['id'])
        self.assertEqual(expected_record['version'], result['version'])


class TestStorageService_WithSideEffects(TestOsduServiceBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_records = []

    def test_001_create_records(self):
        test_data_file = 'tests/test_data/test_create_single_record.json'
        with open(test_data_file, 'r') as _file:
            records_to_store = json.load(_file)

        result = self.osdu.storage.store_records(records_to_store)
        type(self).test_records = result['recordIds']

        self.assertEqual(len(records_to_store), result['recordCount'])

    def test_002_delete_record_only_soft_deletes(self):
        """Verify record is only soft deleted."""
        # Arrange
        record_id = self.test_records[0]
        record_was_deleted = False
        record_still_exists = False

        # Act
        record_was_deleted = self.osdu.storage.delete_record(record_id)
        record_still_has_versions = dict(self.osdu.storage.get_all_record_versions(
            record_id)).get('recordId') == record_id
        with self.assertRaises(requests.RequestException) as context:
            self.osdu.storage.get_record(record_id)  # Should throw exception

        # Assert
        self.assertTrue(record_was_deleted)
        self.assertTrue(record_still_has_versions)
        self.assertEqual(404, context.exception.response.status_code)

    def test_003_purge_record(self):
        # Arrange
        record_id = self.test_records[0]
        record_was_purged = False

        # Act
        record_was_purged = self.osdu.storage.purge_record(record_id)
        if record_was_purged:
            self.test_records.remove(record_id)
        with self.assertRaises(requests.RequestException) as context:
            self.osdu.storage.get_all_record_versions(record_id)

        # Assert
        self.assertTrue(record_was_purged)
        self.assertEqual(404, context.exception.response.status_code)

    @classmethod
    def tearDownClass(cls):
        for record_id in cls.test_records:
            cls.osdu.storage.purge_record(record_id)
        super().tearDownClass()
