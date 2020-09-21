""" In order to run these tests, you must provide an appropriate `user` and `password`. The password
can be set locally by setting the environment variable OSDU_PASSWORD. If using
VS Code, then you can set this in your local `.env` file in your workspace directory to easily
switch between OSDU environments.
"""

import unittest
import json
from functools import reduce
import sys
from osdu.client import AwsOsduClient


class TestOsduClient(unittest.TestCase):

    def test_get_access_token(self):
        osdu = AwsOsduClient()
        token = osdu.token
        self.assertIsNotNone(token)


class TestOsduServiceBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Authenticate once for the test fixture.
        cls.osdu = AwsOsduClient()

    def setUp(self):
        # Reuse the existing fixture-wide token for each test case.
        self.osdu = type(self).osdu
    

class TestSearchService(TestOsduServiceBase):

    def test_simple_search_for_10_items(self): 
        query = {
            "kind": f"opendes:osdu:*:*"
        }
        result = self.osdu.search.query_with_cursor(query, max_results=10)

        self.assertEqual(10, len(result))

    def test_get_all_wells(self):
        query_get_all_wells = {
            "kind": "opendes:osdu:*:0.2.0",
            "query": "data.ResourceTypeID:\"srn:type:master-data/Well:\"",
            "limit": 10
        }

        result = self.osdu.search.query_with_cursor(query_get_all_wells)

        # All results should be wells.
        wells = filter(lambda x : x['type'] == 'well-master', result)

        self.assertCountEqual(wells, result)


    def test_get_all_wellbores(self):
        #Get Wellbores
        query = {
            "kind": "opendes:osdu:*:0.2.0",
            "query": "data.ResourceTypeID:\"srn:type:master-data/Wellbore:\"",
            "limit": 10
        }

        result = self.osdu.search.query_with_cursor(query)

        # All results should be well bores.
        wellbores = filter(lambda x : x['type'] == 'wellbore-master', result)

        self.assertCountEqual(wellbores, result)


    def test_full_text_search(self):
        #Wildcard (*) search
        query = {
            "kind": "opendes:osdu:*:0.2.0",
            "query": "BIR*"
        }
        expected_count = 37

        result = self.osdu.search.query_with_cursor(query)

        self.assertEqual(expected_count, len(result))


    def test_find_well_by_id(self):
        #Search By WellID
        query = {  
            "kind": "opendes:osdu:*:0.2.0",
            "query": "data.Data.IndividualTypeProperties.WellID:\"srn:master-data/Well:8690:\""
        }
        expected_count = 2

        result = self.osdu.search.query_with_cursor(query)

        self.assertEqual(expected_count, len(result))


    def test_query_find_matching_wells_by_id(self):
        # Boolean search with OR
        well_ids = [ 'srn:master-data/Well:8690:', 'srn:master-data/Well:1000:' ]
        query = {
            "kind": "opendes:osdu:*:0.2.0",
            "query": f"data.ResourceID:(\"{well_ids[0]}\" OR \"{well_ids[1]}\")"
        }
        expected_count = len(well_ids)

        result = self.osdu.search.query_with_cursor(query)

        self.assertEqual(expected_count, len(result))
        self.assertIn(result[0]['data']['ResourceID'], well_ids)
        self.assertIn(result[1]['data']['ResourceID'], well_ids)


    def test_find_well_in_country(self):
        #More Boolean search
        query = {
            "kind": "opendes:osdu:*:0.2.0",
            "query": "(data.ResourceID:(\"srn:master-data/Well:8690:\" \
                OR \"srn:master-data/Well:1000:\")) \
                AND (data.Data.IndividualTypeProperties.CountryID: \"srn:master-data/GeopoliticalEntity:Netherlands:\")"
        }
        expected_count = 2

        result = self.osdu.search.query_with_cursor(query)

        self.assertEqual(expected_count, len(result))


    def test_find_welllogs_with_gr_curve(self):
        # WellLog with GR curve
        query = {
            "kind": "opendes:osdu:*:0.2.0",
            "query": "(data.ResourceTypeID: \"srn:type:work-product-component/WellLog:\") AND (data.Data.IndividualTypeProperties.Curves.Mnemonic: GR)"
        }
        expected_count = 100

        result = self.osdu.search.query_with_cursor(query)

        self.assertEqual(expected_count, len(result))


    def test_find_markers_trajectories_for_wellbore(self):
        # Markers and Trajectories for a Wellbore
        query = {
            "kind": "opendes:osdu:*:0.2.0",
            "query": "(data.Data.IndividualTypeProperties.WellboreID: \"srn:master-data/Wellbore:3687:\") AND (data.ResourceTypeID: (\"srn:type:work-product-component/WellboreTrajectory:\" OR \"srn:type:work-product-component/WellboreMarker:\"))"
        }
        expected_count = 2

        result = self.osdu.search.query_with_cursor(query)

        self.assertEqual(expected_count, len(result))


    def test_returned_fields(self):
        query = {
            "kind": "opendes:osdu:*:0.2.1",
            "query": "data.ResourceTypeID:\"srn:type:master-data/Well:\"",
            "limit": 10,
            "returnedFields": ["data.Data.IndividualTypeProperties.CountryID"]
        }

        result = self.osdu.search.query_with_cursor(query)
        
        returned_fields = lambda d : list(d.keys())
        # self.assertListEqual(['data'], returned_fields(result[0]))
        self.assertListEqual(['Data.IndividualTypeProperties.CountryID'], returned_fields(result[0]['data']))


    def test_find_number_of_wellbores_for_a_well(self):
        # Get the number of wellbores for a well 
        query = {
            "kind": "opendes:osdu:*:0.2.0",
            "query": "data.Data.IndividualTypeProperties.WellID:\"srn:master-data/Well:3687:\"",
            "returnedFields": [""],
            "limit": 1
        }
        expected_count = 3

        result = self.osdu.search.query_with_cursor(query)

        self.assertEqual(expected_count, len(result))



class TestStorageService(TestOsduServiceBase):

    def test_query_all_kinds(self):
        result = self.osdu.storage.query_all_kinds()

        self.assertTrue(len(result) > 100)


    def test_get_record(self):
        record_id_query = {
            "kind": "*:*:*:*",
            "limit": 1,
            "returnedFields": ["id"]
        }
        record_id = self.osdu.search.query_with_cursor(record_id_query, max_results=1)[0]['id']

        result = self.osdu.storage.get_record(record_id)

        self.assertEqual(record_id, result['id'])


    def test_create_delete_single_record(self):
        test_data_file = 'tests/test_data/test_create_single_record.json'
        with open(test_data_file, 'r') as _file:
            record = json.load(_file)

        result = self.osdu.storage.store_record([record])
        record_ids = result['recordIds']
        print('Records created: ')
        print(result['recordIds'])

        # Clean up.
        del_results = []
        for rec_id in record_ids:
            isSuccess = self.osdu.storage.delete_record(rec_id)
            del_results.append(isSuccess)

        self.assertEqual(1, result['recordCount'])
        # self.assertEqual([], result['skippedRecords'])
        # Assert that all deletes succeeded.
        self.assertNotIn(False, del_results)



class TestDeliveryService(TestOsduServiceBase):

    def test_get_signed_urls_wells(self):
        # Arrange
        expected_count = {
            'unprocessed': 0 
        }
        srns_query = {
            "kind": "opendes:osdu:*:0.2.0",
            "query": "(data.Data.IndividualTypeProperties.WellboreID: \"srn:master-data/Wellbore:*:\") AND (data.ResourceTypeID: (\"srn:type:work-product-component/WellboreTrajectory:\" OR \"srn:type:work-product-component/WellboreMarker:\"))",
            "returnedFields": ["data.Data.GroupTypeProperties.Files"]
        }
        srns_results = self.osdu.search.query_with_cursor(srns_query, max_results=3)
        srns = reduce(
            (lambda a, b : a + b), 
            map(
                lambda result : result['data']['Data.GroupTypeProperties.Files'], 
                srns_results
            )
        )
        expected_count['processed'] = len(srns)

        # Act
        result = self.osdu.delivery.get_signed_urls(srns)

        # Assert
        self.assertEqual(expected_count['processed'], len(result['processed']))
        self.assertEqual(expected_count['unprocessed'], len(result['unprocessed']))



if __name__ == '__main__':
    unittest.main()