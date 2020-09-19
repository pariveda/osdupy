# osdupy

A simple python client for the [OSDU](https://community.opengroup.org/osdu) data platform.

## Usage

### Installation

```bash
pip install osdupy
```

### Example

#### Initialize the client

If your environment variables (below) have been set, then client.get_client() can be called with no args.
Environment variables: `OSDU_API_URL`, `OSDU_CLIENT_ID`, `OSDU_USER`, `OSDU_PASSWORD`

```python
from osdu import client

osdu = client.get_client()
```

If you have not set the above environment variales, then you will need to pass any undefined as args to `client.get_client()`

```python
from getpass import getpass()
from osdu import client

api_url = 'https://your_api_url'
client_id = 'YOURCLIENTID'
user = 'username@testing.com'
password = getpass()
osdu = client.get_client(api_url, client_id, user, password)
```

#### Use the client

```python
# Search for records by query.
query = {
    "kind": f"opendes:osdu:*:*"
}
result = osdu.search.query_with_cursor(query, max_results=10)

# Get a record.
record_id = 'opendes:doc:01255650acef4930a04048dbb4b559d0'
result = osdu.storage.get_record(record_id)

```

See [tests](tests/tests.py) for more copmrehensive usage examples.
