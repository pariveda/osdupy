# Release Notes

## `0.1.0`

**Release Date**: 2020.10.13

Split the clients into separate modules to eliminate the boto3 dependency for those who don't need the `AwsOsduClient`

The change is very minor, and the only impacts will be:

1. `osdupy` will no longer explicitly depend on `boto3` . You will instead need to separately install `boto3` if you intend to use the `AwsOsduClient` class.
2. Client imports will have require additional namespace on import statements:

`v0.0.10`

```python
from osdu.client import AwsOsduClient
from osdu.client import SimpleOsduClient
```

`v0.1.0`

```python
from osdu.client.aws import AwsOsduClient
from osdu.client.simple import SimpleOsduClient
```
