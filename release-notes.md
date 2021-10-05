# Release Notes

## `0.3.0`

**Release Date**: 2021-10-01

Changes by Chris Parsons from Petrosys to include Entitlements service.

## `0.2.1`

**Release Date**: 2021-10-01

Changes by Chris Parsons from Petrosys to include secret hash for more security around Cognito Authorization.

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

### `0.1.1`

**Release Date**: 2020.10.19

Added `profile` constructor arg and class property for AwsOsduClient to specify the AWS profile to be used when connecting to Cognito to obtain access token.
