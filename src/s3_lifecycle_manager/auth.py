"""
AWS Credential Verification Module
==================================

This module provides functionality to verify if AWS credentials
are correctly configured.

Example usage:
--------------
    from auth import verify_aws_credentials

    verify_aws_credentials()

Dependencies:
-------------
- boto3

Author:
-------
- Rodrigo de Souza Rampazzo <rosorzz@protonmail.com>
- GitHub: https://github.com/rzz0

License:
--------
MIT License
"""

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from .logger import configure_logging, get_logger

# Configure logger
configure_logging()
logger = get_logger(__name__)


def verify_aws_credentials():
    """
    Verifies if AWS credentials are correctly configured.

    This function attempts to create a boto3 client to verify if
    credentials are already configured. If it succeeds, the credentials
    are configured correctly. If it fails, the credentials are missing
    or incorrect.
    """
    try:
        boto3.client("sts").get_caller_identity()
        logger.info("AWS credentials are correctly configured.")
        return True
    except (NoCredentialsError, PartialCredentialsError):
        logger.error("AWS credentials are not configured correctly.")
        return False


if __name__ == "__main__":
    verify_aws_credentials()
