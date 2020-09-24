# osdupy

A simple python client for the [OSDU](https://community.opengroup.org/osdu) data platform.

## Currently supported methods

- search
  - query
  - query_with_paging
- storage
  - query_all_kinds
  - get_record
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

If your environment variables (below) have been set, then client.get_client() can be called with no args.
Environment variables: `OSDU_API_URL`, `OSDU_CLIENT_ID`, `OSDU_USER`, `OSDU_PASSWORD`

```python
from osdu.client import AwsOsduClient

data_partition = 'opendes'

osdu = AwsOsduClient(data_partition)
```

If you have not set the above environment variales, then you will need to pass any undefined as args when instantiating the client.

```python
from getpass import getpass()
from osdu.client import AwsOsduClient

api_url = 'https://your_api_url'
client_id = 'YOURCLIENTID'
user = 'username@testing.com'
password = getpass()
data_partition = 'yourpartition'

osdu = AwsOsduClient(data_partition, api_url, client_id, user, password)
```

### Use the client

```python
# Search for records by query.
query = {
    "kind": f"opendes:osdu:*:*"
}
result = osdu.search.query(query)
# { results: [ {...}, .... ], totalCount: ##### }


# Get a record.
record_id = 'opendes:doc:123456789'
result = osdu.storage.get_record(record_id)
# { 'id': 'opendes:doc:123456789', 'kind': ..., 'data': {...}, 'acl': {...}, .... }
```

See [tests](tests/tests.py) for more copmrehensive usage examples.
