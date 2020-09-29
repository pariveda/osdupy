# osdupy

A simple python client for the [OSDU](https://community.opengroup.org/osdu) data platform.

## Currently supported methods

- search
  - query
  - query_with_paging
- storage
  - query_all_kinds
  - get_record
  - get_all_record_versions
  - get_record_version
  - store_records
  - delete_record
- delivery
  - get_signed_urls

## Installation

```bash
pip install osdupy
```

## Usage

### Initialize the client

The only required argument is `data_partition`. If your environment variables (below) have been set, then client can be instantiated with only `data_partition` as an argument.
Environment variables: 
1. `OSDU_API_URL`
1. `OSDU_CLIENT_ID`
1. `OSDU_USER`
1. `OSDU_PASSWORD`

```python
from osdu.client import AwsOsduClient

data_partition = 'opendes'

osdu = AwsOsduClient(data_partition)
```

If you have not set the above environment variales—or you have only set some—then you will need to pass any undefined as args when instantiating the client.

```python
from getpass import getpass
from osdu.client import AwsOsduClient

api_url = 'https://your.api.url.com'  # Must be base URL only
client_id = 'YOURCLIENTID'
user = 'username@testing.com'
password = getpass()
data_partition = 'yourpartition'

osdu = AwsOsduClient(data_partition,  
    api_url=api_url,  
    client_id=client_id,  
    user=user,  
    password=password)
```

### Use the client

Below are just a few usage examples. See [tests](https://github.com/pariveda/osdupy/blob/master/tests/tests.py) for more copmrehensive usage examples.

#### Search for records by query

```python
query = {
    "kind": f"opendes:osdu:*:*"
}
result = osdu.search.query(query)
# { results: [ {...}, .... ], totalCount: ##### }
```

#### Search with paging

For result sets larger than 1,000 records, use the query with paging method.

```python
page_size = 100 # Number of records per page (1-1000)
query = {
    "kind": f"opendes:osdu:*:*",
    "limit": page_size
}
result = osdu.search.query_with_paging(query)

# Iterate over the pages to do something with the results.
for page, total_count in result:
    for record in page:
        # Do stuff with record...
```

#### Get a record

```python
record_id = 'opendes:doc:123456789'
result = osdu.storage.get_record(record_id)
# { 'id': 'opendes:doc:123456789', 'kind': ..., 'data': {...}, 'acl': {...}, .... }
```

#### Upsert records

```python
new_or_updated_record = './record-123.json'
with open(new_or_updated_record, 'r') as _file:
    record = json.load(_file)

result = osdu.storage.store_records([record])

```
