"""
AWS Credential Configuration Module
===================================

This module provides functionality to configure AWS credentials
by prompting the user for input if necessary. It includes the ability
to save the credentials to a configuration file for future use.

Example usage:
--------------
    from auth import configure_aws_credentials

    configure_aws_credentials()

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

import os
from getpass import getpass
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from .logger import configure_logging, get_logger

# Configure logger
configure_logging()
logger = get_logger(__name__)


def configure_aws_credentials():
    """
    Configures AWS credentials by prompting the user if necessary.

    This function attempts to create a boto3 client to verify if credentials are
    already configured. If not, it prompts the user to enter their AWS credentials
    and optionally saves them to a configuration file for future use.
    """
    try:
        # Try to create a boto3 client to see if credentials are already configured
        boto3.client('sts').get_caller_identity()
        logger.info("AWS credentials are already configured.")
    except (NoCredentialsError, PartialCredentialsError):
        logger.info(
            "AWS credentials not found. Please enter your AWS credentials.")
        aws_access_key_id = input("AWS Access Key ID: ").strip()
        aws_secret_access_key = getpass("AWS Secret Access Key: ").strip()
        aws_session_token = getpass(
            "AWS Session Token (leave empty if not applicable): ").strip()

        if not aws_access_key_id or not aws_secret_access_key:
            logger.error(
                "AWS Access Key ID and Secret Access Key are required.")
            return

        # Set credentials in environment variables
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        if aws_session_token:
            os.environ['AWS_SESSION_TOKEN'] = aws_session_token

        # Optionally, save the credentials to a file for future use
        save_credentials = input(
            "Do you want to save these credentials for future use? (y/n): ").strip().lower()
        if save_credentials == 'y':
            save_credentials_to_file(
                aws_access_key_id, aws_secret_access_key, aws_session_token)


def save_credentials_to_file(aws_access_key_id, aws_secret_access_key, aws_session_token):
    """
    Saves AWS credentials to a configuration file.

    :param aws_access_key_id: AWS Access Key ID
    :type aws_access_key_id: str
    :param aws_secret_access_key: AWS Secret Access Key
    :type aws_secret_access_key: str
    :param aws_session_token: AWS Session Token (optional)
    :type aws_session_token: str
    """
    config_file = os.path.expanduser('~/.aws/credentials')
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    with open(config_file, 'w', encoding='utf-8') as file:
        file.write("[default]\n")
        file.write(f"aws_access_key_id = {aws_access_key_id}\n")
        file.write(f"aws_secret_access_key = {aws_secret_access_key}\n")
        if aws_session_token:
            file.write(f"aws_session_token = {aws_session_token}\n")
    logger.info(f"Credentials saved to {config_file}")


if __name__ == "__main__":
    configure_aws_credentials()
