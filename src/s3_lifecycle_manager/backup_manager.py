"""
S3 Lifecycle Backup Manager
===========================

This module provides functionalities to manage backups of S3
ucket lifecycle policies. It includes methods to export, restore,
and list lifecycle policies for S3 buckets.

Example usage:
--------------
    from s3_lifecycle_backup_manager import S3LifecycleBackupManager

    backup_manager = S3LifecycleBackupManager('./backups')
    backup_manager.export_lifecycle_policies(lifecycle_policies)
    backup_manager.restore_lifecycle_policies('bucket1')

Dependencies:
-------------
- boto3

Classes:
    S3LifecycleBackupManager: Manages backups of S3 bucket lifecycle
    policies.

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
from typing import List, Dict
import boto3
from botocore.exceptions import ClientError
from .logger import get_logger


class S3LifecycleBackupManager:
    """
    Manages backups of S3 bucket lifecycle policies.
    """

    def __init__(self, backup_dir: str):
        self.s3_client = boto3.client("s3")
        self.backup_dir = backup_dir
        self.logger = get_logger(__name__)

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

    def export_lifecycle_policies(self, lifecycle_policies: Dict[str, List[Dict]]):
        """
        Exports the lifecycle policies of specified buckets
        to backup files.

        :param lifecycle_policies: Dictionary of bucket names and their lifecycle policies.
        :type lifecycle_policies: Dict[str, List[Dict]]
        """
        for bucket, rules in lifecycle_policies.items():
            if not rules:
                self.logger.info(
                    "No lifecycle configuration to export for bucket %s", bucket
                )
                continue
            backup_file = os.path.join(
                self.backup_dir, f"{bucket}_lifecycle_backup.json"
            )
            try:
                with open(backup_file, "w", encoding="utf-8") as file:
                    json.dump(rules, file, ensure_ascii=False, indent=4)
                self.logger.info(
                    "Exported lifecycle policy for bucket %s to %s", bucket, backup_file
                )
            except IOError as error:
                self.logger.error(
                    "Failed to write backup file %s: %s", backup_file, error
                )

    def restore_lifecycle_policies(self, bucket_name: str):
        """
        Restores the lifecycle policy of a bucket from a backup file.

        :param bucket_name: Name of the bucket to restore policies.
        :type bucket_name: str
        """
        backup_file = os.path.join(
            self.backup_dir, f"{bucket_name}_lifecycle_backup.json"
        )
        if not os.path.exists(backup_file):
            self.logger.error("Backup file %s does not exist", backup_file)
            return

        try:
            with open(backup_file, "r", encoding="utf-8") as file:
                rules = json.load(file)
        except IOError as error:
            self.logger.error("Error reading backup file %s: %s", backup_file, error)
            return

        try:
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=bucket_name, LifecycleConfiguration={"Rules": rules}
            )
            self.logger.info(
                "Restored lifecycle policy for bucket %s from %s",
                bucket_name,
                backup_file,
            )
        except ClientError as error:
            self.logger.error(
                "Failed to restore lifecycle policy for bucket %s: %s",
                bucket_name,
                error,
            )

    def list_backups(self) -> List[str]:
        """
        Lists all available backup files.

        :returns: List of backup file names.
        :rtype: List[str]
        """
        return [
            f
            for f in os.listdir(self.backup_dir)
            if f.endswith("_lifecycle_backup.json")
        ]
