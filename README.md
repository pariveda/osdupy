# osdupy

A simple python client for the [OSDU](https://community.opengroup.org/osdu) data platform.

## Contents

- [Clients](#clients)
  - [SimpleOsduClient](#simpleosduclient)
  - [AwsOsduClient](#awsosduclient)
- [Currently supported methods](#currently-supported-methods)
- [Installation](#installation)
- [Tests](#tests)
- [Usage](#usage)
  - [Instantiating the SimpleOsduClient](#instantiating-the-simpleosduclient)
  - [Instantiating the AwsOsduClient](#instantiating-the-awsosduclient)
  - [Using the client](#using-the-client)
    - [Search for records by query](#search-for-records-by-query)
    - [Search with paging](#search-with-paging)
    - [Get a record](#get-a-record)
    - [Upsert records](#upsert-records)
- [Release Notes](release-notes.md)

## Clients

Choose the client that best meets your needs. The same methods are all supported for each.

### SimpleOsduClient

BYOT: Bring your own token. Great for backend service or business logic that supplements a
front-end application.

This client assumes you are obtaining a token yourself (e.g. via your application's
login form or otheer mechanism. With this SimpleOsduClient, you simply provide that token.
With this simplicity, you are also then respnsible for reefreeshing the token as needed and
re-instantiating the client with the new token.

### AwsOsduClient

**Requires**: `boto3==1.15.*`

Good for batch tasks that don't have an interactive front-end. Token management is handled
with the boto3 library directly through the Cognito service. You have to supply additional arguments for this.

## Currently supported methods

- [search](osdu/search.py)
  - query
  - query_with_paging
- [storage](osdu/storage.py)
  - query_all_kinds
  - get_record
  - get_all_record_versions
  - get_record_version
  - store_records
  - delete_record
- [delivery](osdu/delivery.py)
  - get_signed_urls

## Installation

```bash
pip install osdupy
```

## Tests

Run unit tests

```bash
python -m unittest -v tests.unit
```

Run integration tests

```bash
python -m unittest -v tests.integration
```

## Usage

### Instantiating the SimpleOsduClient

If environment variable `OSDU_API_URL` is set, then it does not need to be passed as an argument. Otherwise it must be passed as keyword argument.

```python
from osdu.client.simple import SimpleOsduClient

data_partition = 'opendes'
token = 'token-received-from-front-end-app'

# With env var `OSDU_API_URL` set in current environment.
osdu = SimpleOsduClient(data_partition, token)

# Without env var set.
api_url = 'https://your.api.base_url.com'
osdu = SimpleOsduClient(data_partition, token, api_url=api_url)

```

### Instantiating the AwsOsduClient

The only required argument is `data_partition`. If your environment variables (below) have been set, then client can be instantiated with only `data_partition` as an argument.
Environment variables:

1. `OSDU_API_URL`
1. `OSDU_CLIENT_ID`
1. `OSDU_USER`
1. `OSDU_PASSWORD`
1. `AWS_PROFILE`
1. `AWS_SECRETHASH`

```python
from osdu.client.aws import AwsOsduClient

data_partition = 'opendes'

osdu = AwsOsduClient(data_partition)
```

If you have not set the above environment variales—or you have only set some—then you will need to pass any undefined as args when instantiating the client.

```python
from getpass import getpass
from osdu.client.aws import AwsOsduClient

api_url = 'https://your.api.url.com'  # Must be base URL only
client_id = 'YOURCLIENTID'
user = 'username@testing.com'
password = getpass()
data_partition = 'osdu'
profile = 'osdu-dev'

message = user + client_id
dig = hmac.new(client_secret.encode('UTF-8'), msg=message.encode('UTF-8'),
               digestmod=hashlib.sha256).digest()
secretHash = base64.b64encode(dig).decode()



osdu = AwsOsduClient(data_partition,
    api_url=api_url,
    client_id=client_id,
    user=user,
    password=password,
    secret_hash=secretHash,
    profile=profile)
```

### Using the client

Below are just a few usage examples. See [integration tests](https://github.com/pariveda/osdupy/blob/master/tests/tests_integration.py) for more copmrehensive usage examples.

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
