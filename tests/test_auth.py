"""
Test Suite for AWS Credential Configuration
===========================================

This module contains unit tests for the AWS credential configuration functions.
It tests the functionalities such as checking if AWS credentials are configured and
saving credentials to a file.

Dependencies:
-------------
- unittest
- unittest.mock
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
import sys
from io import StringIO
import unittest
from unittest.mock import patch
from s3_lifecycle_manager.auth import configure_aws_credentials, save_credentials_to_file


class TestAWSCredentialConfiguration(unittest.TestCase):
    """Tests for AWS credential configuration functions."""

    @patch('s3_lifecycle_manager.auth.boto3.client')
    def test_configure_aws_credentials_already_configured(self, mock_boto_client):
        """Test when AWS credentials are already configured."""
        # Simula credenciais já configuradas
        mock_boto_client().get_caller_identity.return_value = {
            'UserId': 'test-user',
            'Account': 'test-account',
            'Arn': 'arn:aws:iam::test-account:user/test-user'
        }

        with patch('builtins.input', return_value=''), \
                patch('getpass.getpass', return_value=''):
            captured_output = self._get_output(configure_aws_credentials)
            mock_boto_client().get_caller_identity.assert_called_once()
            # Verifica se a mensagem correta foi impressa
            self.assertIn(
                "AWS credentials are already configured.", captured_output)

    @patch('s3_lifecycle_manager.auth.os.makedirs')
    @patch('s3_lifecycle_manager.auth.open', new_callable=unittest.mock.mock_open)
    def test_save_credentials_to_file(self, mock_open, mock_makedirs):
        """Test saving AWS credentials to a file."""
        save_credentials_to_file(
            'test-access-key-id', 'test-secret-access-key', 'test-session-token')

        mock_makedirs.assert_called_once_with(
            os.path.expanduser('~/.aws'), exist_ok=True)
        mock_open.assert_called_once_with(os.path.expanduser(
            '~/.aws/credentials'), 'w', encoding='utf-8')
        mock_open().write.assert_any_call("[default]\n")
        mock_open().write.assert_any_call("aws_access_key_id = test-access-key-id\n")
        mock_open().write.assert_any_call(
            "aws_secret_access_key = test-secret-access-key\n")
        mock_open().write.assert_any_call("aws_session_token = test-session-token\n")

    def _get_output(self, func):
        """Helper function to capture printed output of a function."""
        output = StringIO()
        sys.stdout = output
        func()
        sys.stdout = sys.__stdout__
        return output.getvalue()


if __name__ == '__main__':
    unittest.main()
