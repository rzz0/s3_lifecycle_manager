"""
Test Suite for S3LifecycleManager
=================================

This module contains unit tests for the S3LifecycleManager class. It tests the functionalities
such as listing buckets, retrieving lifecycle policies, processing buckets, and saving policies
to a CSV file.

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
import unittest
from unittest.mock import patch, MagicMock
import csv
from botocore.exceptions import ClientError
from s3_lifecycle_manager.manager import S3LifecycleManager
from s3_lifecycle_manager.logger import configure_logging


class TestS3LifecycleManager(unittest.TestCase):
    """Tests for the S3LifecycleManager class."""

    def setUp(self):
        """Set up the test environment with a mock S3 client."""
        patcher = patch('boto3.client')
        self.addCleanup(patcher.stop)
        self.mock_boto_client = patcher.start()
        self.mock_s3 = MagicMock()
        self.mock_boto_client.return_value = self.mock_s3
        self.manager = S3LifecycleManager()
        configure_logging()

    def test_list_buckets(self):
        """Test listing S3 buckets."""
        self.mock_s3.list_buckets.return_value = {
            'Buckets': [{'Name': 'test-bucket'}, {'Name': 'empty-bucket'}]
        }

        buckets = self.manager.list_buckets()
        self.assertEqual(len(buckets), 2)
        self.assertTrue(
            any(bucket['Name'] == 'test-bucket' for bucket in buckets))
        self.assertTrue(
            any(bucket['Name'] == 'empty-bucket' for bucket in buckets))

    def test_get_lifecycle_policy(self):
        """Test retrieving lifecycle policy for a bucket."""
        self.mock_s3.get_bucket_lifecycle_configuration.return_value = {
            'Rules': [{'ID': 'rule1'}]
        }

        rules = self.manager.get_lifecycle_policy('test-bucket')
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0]['ID'], 'rule1')

    def test_get_lifecycle_policy_client_error(self):
        """Test handling of ClientError when retrieving lifecycle policy."""
        self.mock_s3.get_bucket_lifecycle_configuration.side_effect = ClientError(
            {"Error": {
                "Code": "NoSuchLifecycleConfiguration",
                "Message": "The lifecycle configuration does not exist."
            }},
            "GetBucketLifecycleConfiguration"
        )

        rules = self.manager.get_lifecycle_policy('non-existent-bucket')
        self.assertEqual(len(rules), 0)

    def test_get_lifecycle_policy_access_denied(self):
        """Test handling of AccessDenied error when retrieving lifecycle policy."""
        self.mock_s3.get_bucket_lifecycle_configuration.side_effect = ClientError(
            {"Error": {"Code": "AccessDenied", "Message": "Access Denied"}
             }, "GetBucketLifecycleConfiguration"
        )

        rules = self.manager.get_lifecycle_policy('test-bucket')
        self.assertEqual(len(rules), 0)

    def test_process_buckets_no_rules(self):
        """Test processing of buckets with no lifecycle rules."""
        self.mock_s3.list_buckets.return_value = {
            'Buckets': [{'Name': 'test-bucket'}, {'Name': 'empty-bucket'}]
        }
        self.mock_s3.get_bucket_lifecycle_configuration.side_effect = ClientError(
            {"Error": {
                "Code": "NoSuchLifecycleConfiguration",
                "Message": "The lifecycle configuration does not exist."
            }},
            "GetBucketLifecycleConfiguration"
        )

        self.manager.process_buckets()
        self.assertEqual(len(self.manager.policies), 2)
        bucket_names = [policy['Bucket'] for policy in self.manager.policies]
        self.assertIn('test-bucket', bucket_names)
        self.assertIn('empty-bucket', bucket_names)
        self.assertEqual(self.manager.policies[0]['Status'], 'No Rules')

    def test_process_buckets_with_rules(self):
        """Test processing of buckets with lifecycle rules."""
        self.mock_s3.list_buckets.return_value = {
            'Buckets': [{'Name': 'test-bucket'}, {'Name': 'empty-bucket'}]
        }
        self.mock_s3.get_bucket_lifecycle_configuration.side_effect = [
            {'Rules': [
                {'ID': 'rule1',
                 'Status': 'Enabled',
                 'Filter': {'Prefix': ''},
                 'Transitions': [],
                 'Expiration': {},
                 'NoncurrentVersionTransitions': [],
                 'NoncurrentVersionExpiration': {},
                 'AbortIncompleteMultipartUpload': {}}]},
            ClientError({
                "Error": {"Code": "NoSuchLifecycleConfiguration",
                        "Message": "The lifecycle configuration does not exist."}},
                        "GetBucketLifecycleConfiguration")
        ]

        self.manager.process_buckets()
        self.assertEqual(len(self.manager.policies), 2)
        self.assertEqual(self.manager.policies[0]['Status'], 'Enabled')
        self.assertEqual(self.manager.policies[0]['ID'], 'rule1')

    def test_analyze_rule(self):
        """Test analysis of a lifecycle rule."""
        rule = {
            'Status': 'Enabled',
            'ID': 'rule1',
            'Filter': {'Prefix': 'myprefix'},
            'Transitions': [{'Days': 30, 'StorageClass': 'GLACIER'}],
            'Expiration': {'Days': 365},
            'NoncurrentVersionTransitions': [{'NoncurrentDays': 30, 'StorageClass': 'GLACIER'}],
            'NoncurrentVersionExpiration': {'NoncurrentDays': 365},
            'AbortIncompleteMultipartUpload': {'DaysAfterInitiation': 7}
        }

        result = self.manager.analyze_rule(rule)
        expected = {
            'Status': 'Enabled',
            'ID': 'rule1',
            'Prefix': 'myprefix',
            'Transitions': '30 days to GLACIER',
            'ExpirationDays': 365,
            'NoncurrentVersionTransitions': '30 days to GLACIER',
            'NoncurrentVersionExpirationDays': 365,
            'AbortIncompleteMultipartUploadDays': 7
        }

        self.assertEqual(result, expected)

    def test_save_policies_csv(self):
        """Test saving policies to a CSV file."""
        self.manager.policies = [
            {
                'Bucket': 'test-bucket',
                'Status': 'No Rules',
                'ID': 'N/A',
                'Prefix': 'N/A',
                'Transitions': 'N/A',
                'ExpirationDays': 'N/A',
                'NoncurrentVersionTransitions': 'N/A',
                'NoncurrentVersionExpirationDays': 'N/A',
                'AbortIncompleteMultipartUploadDays': 'N/A'
            }
        ]
        self.manager.save_policies_csv('test_policies.csv')
        with open('test_policies.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]['Bucket'], 'test-bucket')

    def test_save_policies_csv_no_policies(self):
        """Test behavior when there are no policies to save."""
        self.manager.policies = []
        with patch('logging.Logger.warning') as mock_warning:
            self.manager.save_policies_csv('test_policies.csv')
            mock_warning.assert_called_with("No policies to save.")

    def test_process_and_save_buckets(self):
        """Test processing buckets and saving policies to a CSV file."""
        self.mock_s3.list_buckets.return_value = {
            'Buckets': [{'Name': 'test-bucket'}, {'Name': 'empty-bucket'}]
        }
        self.mock_s3.get_bucket_lifecycle_configuration.side_effect = [
            {'Rules': [
                {'ID': 'rule1',
                 'Status': 'Enabled',
                 'Filter': {'Prefix': ''},
                 'Transitions': [],
                 'Expiration': {},
                 'NoncurrentVersionTransitions': [],
                 'NoncurrentVersionExpiration': {},
                 'AbortIncompleteMultipartUpload': {}}]},
            ClientError({
                "Error": {
                    "Code": "NoSuchLifecycleConfiguration",
                        "Message": "The lifecycle configuration does not exist."
                        }
            },
                "GetBucketLifecycleConfiguration")
        ]

        self.manager.process_buckets()
        self.manager.save_policies_csv('test_policies.csv')

        with open('test_policies.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['Bucket'], 'test-bucket')
            self.assertEqual(rows[1]['Bucket'], 'empty-bucket')
            self.assertEqual(rows[0]['ID'], 'rule1')
            self.assertEqual(rows[1]['Status'], 'No Rules')


if __name__ == '__main__':
    unittest.main()
