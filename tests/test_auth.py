"""
Test Suite for AWS Credential Verification
==========================================

This module contains unit tests for the AWS credential verification function.
It tests the functionalities such as checking if AWS credentials are correctly
configured, missing, or partially configured.

Dependencies:
-------------
- unittest.mock
- pytest
- boto3
- botocore.exceptions

Author:
-------
- Rodrigo de Souza Rampazzo <rosorzz@protonmail.com>
- GitHub: https://github.com/rzz0

License:
--------
MIT License
"""

from unittest.mock import patch
import pytest
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from s3_lifecycle_manager.auth import verify_aws_credentials


@patch("s3_lifecycle_manager.auth.boto3.client")
def test_verify_aws_credentials_success(mock_boto_client):
    """
    Test when AWS credentials are configured correctly.

    This test simulates a scenario where AWS credentials are correctly
    configured by mocking the boto3 client and verifying that the function
    `verify_aws_credentials` returns True.
    """
    mock_boto_client.return_value.get_caller_identity.return_value = {}
    assert verify_aws_credentials() is True


@patch("s3_lifecycle_manager.auth.boto3.client")
def test_verify_aws_credentials_no_credentials(mock_boto_client):
    """
    Test when AWS credentials are missing.

    This test simulates a scenario where AWS credentials are missing by
    raising a NoCredentialsError and verifying that the function
    `verify_aws_credentials` returns False.
    """
    mock_boto_client.return_value.get_caller_identity.side_effect = NoCredentialsError()
    assert verify_aws_credentials() is False


@patch("s3_lifecycle_manager.auth.boto3.client")
def test_verify_aws_credentials_partial_credentials(mock_boto_client):
    """
    Test when AWS credentials are partially configured.

    This test simulates a scenario where AWS credentials are partially
    configured by raising a PartialCredentialsError and verifying that the
    function `verify_aws_credentials` returns False.
    """
    mock_boto_client.return_value.get_caller_identity.side_effect = (
        PartialCredentialsError(provider="aws", cred_var="AWS_SECRET_ACCESS_KEY")
    )
    assert verify_aws_credentials() is False


if __name__ == "__main__":
    pytest.main()
