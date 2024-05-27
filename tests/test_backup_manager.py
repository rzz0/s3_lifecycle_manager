"""
Test Suite for S3LifecycleBackupManager
=======================================

This module contains unit tests for the S3LifecycleBackupManager class. It tests the functionalities
such as exporting, restoring, and listing lifecycle policies for S3 buckets.

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
import json
import unittest
from unittest.mock import patch, MagicMock
from s3_lifecycle_manager.backup_manager import S3LifecycleBackupManager


class TestS3LifecycleBackupManager(unittest.TestCase):
    """Tests for the S3LifecycleBackupManager class."""

    def setUp(self):
        """Set up the test environment with a mock S3 client and a backup directory."""
        self.patcher = patch(
            's3_lifecycle_manager.backup_manager.boto3.client')
        self.mock_boto_client = self.patcher.start()
        self.mock_s3_client = MagicMock()
        self.mock_boto_client.return_value = self.mock_s3_client
        self.backup_manager = S3LifecycleBackupManager('./backups')
        self.bucket_names = ['test-bucket-1', 'test-bucket-2']

        # Create backup directory if it does not exist
        if not os.path.exists('./backups'):
            os.makedirs('./backups')

    def tearDown(self):
        """Clean up the backup directory after each test."""
        self.patcher.stop()
        for file_name in os.listdir('./backups'):
            file_path = os.path.join('./backups', file_name)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        os.rmdir('./backups')

    def test_export_lifecycle_policies(self):
        """Test exporting lifecycle policies for specified buckets."""
        # Mock lifecycle policy
        lifecycle_policy = {
            "Rules": [
                {
                    "ID": "test-rule",
                    "Filter": {"Prefix": ""},
                    "Status": "Enabled",
                    "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"}]
                }
            ]
        }
        self.mock_s3_client.get_bucket_lifecycle_configuration.side_effect = [
            {'Rules': lifecycle_policy['Rules']},
            {'Rules': []}  # Simulate no lifecycle configuration for test-bucket-2
        ]

        self.backup_manager.export_lifecycle_policies(self.bucket_names)

        # Verificar se os arquivos de backup foram criados
        backup_files = self.backup_manager.list_backups()
        self.assertIn('test-bucket-1_lifecycle_backup.json', backup_files)

        # test-bucket-2 should not have a backup file as it has no lifecycle configuration
        self.assertNotIn('test-bucket-2_lifecycle_backup.json', backup_files)

        # Verificar o conteúdo do arquivo de backup
        with open(os.path.join(self.backup_manager.backup_dir,
                               'test-bucket-1_lifecycle_backup.json'),
                  mode='r',
                  encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(data, lifecycle_policy['Rules'])

    def test_restore_lifecycle_policies(self):
        """Test restoring lifecycle policies from backup files."""
        # Mock lifecycle policy
        lifecycle_policy = {
            "Rules": [
                {
                    "ID": "test-rule",
                    "Filter": {"Prefix": ""},
                    "Status": "Enabled",
                    "Transitions": [{"Days": 30, "StorageClass": "STANDARD_IA"}]
                }
            ]
        }

        backup_file = os.path.join(
            self.backup_manager.backup_dir, 'test-bucket-1_lifecycle_backup.json')
        os.makedirs(self.backup_manager.backup_dir, exist_ok=True)
        with open(backup_file, 'w', encoding='utf-8') as file:
            json.dump(lifecycle_policy['Rules'],
                      file, ensure_ascii=False, indent=4)

        self.backup_manager.restore_lifecycle_policies('test-bucket-1')

        # Verificar se a política de ciclo de vida foi restaurada
        self.mock_s3_client.put_bucket_lifecycle_configuration.assert_called_with(
            Bucket='test-bucket-1',
            LifecycleConfiguration={'Rules': lifecycle_policy['Rules']}
        )

    def test_list_backups(self):
        """Test listing available backup files."""
        # Configure arquivos de backup
        backup_files = ['test-bucket-1_lifecycle_backup.json',
                        'test-bucket-2_lifecycle_backup.json']
        os.makedirs(self.backup_manager.backup_dir, exist_ok=True)
        for file_name in backup_files:
            open(os.path.join(self.backup_manager.backup_dir, file_name),
                 mode='a', encoding='utf-8').close()

        listed_backups = self.backup_manager.list_backups()
        self.assertEqual(set(listed_backups), set(backup_files))


if __name__ == '__main__':
    unittest.main()
