"""
S3 Lifecycle Backup Manager
===========================

This module provides functionalities to manage backups of S3 bucket lifecycle policies.
It includes methods to export, restore, and list lifecycle policies for S3 buckets.

Example usage:
--------------
    from s3_lifecycle_backup_manager import S3LifecycleBackupManager

    backup_manager = S3LifecycleBackupManager('./backups')
    backup_manager.export_lifecycle_policies(['bucket1', 'bucket2'])
    backup_manager.restore_lifecycle_policies('bucket1')

Dependencies:
-------------
- boto3

Classes:
    S3LifecycleBackupManager: Manages backups of S3 bucket lifecycle policies.

Author:
-------
- Rodrigo de Souza Rampazzo <rosorzz@protonmail.com>
- GitHub: https://github.com/rzz0

License:
--------
MIT License
"""

import json
import os
from typing import List
import boto3
from botocore.exceptions import ClientError
from .logger import get_logger


class S3LifecycleBackupManager:
    """Manages backups of S3 bucket lifecycle policies."""

    def __init__(self, backup_dir: str):
        self.s3_client = boto3.client('s3')
        self.backup_dir = backup_dir
        self.logger = get_logger(__name__)

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

    def export_lifecycle_policies(self, bucket_names: List[str]):
        """Exports the lifecycle policies of specified buckets to backup files."""
        for bucket in bucket_names:
            try:
                policy = self.s3_client.get_bucket_lifecycle_configuration(
                    Bucket=bucket)
                rules = policy.get('Rules', [])
                if not rules:
                    self.logger.info(
                        "No lifecycle configuration to export for bucket %s", bucket)
                    continue
                backup_file = os.path.join(
                    self.backup_dir, f"{bucket}_lifecycle_backup.json")
                with open(backup_file, 'w', encoding='utf-8') as file:
                    json.dump(rules, file, ensure_ascii=False, indent=4)
                self.logger.info(
                    "Exported lifecycle policy for bucket %s to %s", bucket, backup_file)
            except ClientError as error:
                if error.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                    self.logger.info(
                        "No lifecycle configuration found for bucket %s", bucket)
                else:
                    self.logger.error(
                        "Failed to export lifecycle policy for bucket %s: %s", bucket, error)

    def restore_lifecycle_policies(self, bucket_name: str):
        """Restores the lifecycle policy of a bucket from a backup file."""
        backup_file = os.path.join(
            self.backup_dir, f"{bucket_name}_lifecycle_backup.json")
        if not os.path.exists(backup_file):
            self.logger.error("Backup file %s does not exist", backup_file)
            return

        with open(backup_file, 'r', encoding='utf-8') as file:
            rules = json.load(file)

        try:
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration={'Rules': rules}
            )
            self.logger.info(
                "Restored lifecycle policy for bucket %s from %s", bucket_name, backup_file)
        except ClientError as error:
            self.logger.error(
                "Failed to restore lifecycle policy for bucket %s: %s", bucket_name, error)

    def list_backups(self) -> List[str]:
        """Lists all available backup files."""
        return [f for f in os.listdir(self.backup_dir) if f.endswith('_lifecycle_backup.json')]
