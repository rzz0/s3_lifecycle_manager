"""
S3 Lifecycle Manager
====================

This module manages the lifecycle policies of S3 buckets,
listing the buckets and extracting the lifecycle rules to save
in a CSV file. It includes information about buckets that do
not have lifecycle rules.

Example usage:
--------------
    from s3_lifecycle_manager.manager import S3LifecycleManager

    manager = S3LifecycleManager()
    bucket_names = [bucket["Name"] for bucket in manager.list_buckets()]
    manager.process_buckets(bucket_names)
    manager.save_policies_csv('lifecycle_buckets.csv')

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

import csv
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError
from .auth import configure_aws_credentials
from .logger import get_logger
from .lifecycle_policy import LifecyclePolicy


class S3LifecycleManager:
    """Manages the lifecycle policies of S3 buckets."""

    def __init__(self):
        configure_aws_credentials()
        self.s3_client = boto3.client("s3")
        self.policies: List[Dict[str, Any]] = []
        self.logger = get_logger(__name__)

    def list_buckets(self) -> List[Dict[str, Any]]:
        """
        Lists all S3 buckets.

        :returns: List of dictionaries containing bucket information.
        :rtype: List[Dict[str, Any]]
        """
        try:
            buckets = self.s3_client.list_buckets().get("Buckets", [])
            self.logger.info("%d buckets found.", len(buckets))
            return buckets
        except boto3.exceptions.Boto3Error as error:
            self.logger.error("Error listing buckets: %s", error)
            return []

    def get_lifecycle_policy(self, bucket_name: str) -> List[Dict[str, Any]]:
        """
        Gets the lifecycle configuration for a specified bucket.

        :param bucket_name: Name of the bucket.
        :type bucket_name: str
        :returns: List of lifecycle rules, or an empty list if the bucket
        has no lifecycle configuration.
        :rtype: List[Dict[str, Any]]
        """
        try:
            response = self.s3_client.get_bucket_lifecycle_configuration(
                Bucket=bucket_name
            )
            return response.get("Rules", [])
        except ClientError as error:
            if error.response["Error"]["Code"] == "NoSuchLifecycleConfiguration":
                return []
            self.logger.warning(
                "Unable to get the lifecycle policy for bucket %s: %s",
                bucket_name,
                error,
            )
            return []

    def process_buckets(self, bucket_names: List[str]) -> None:
        """
        Processes all buckets and extracts their lifecycle policies.

        :param bucket_names: List of bucket names to process.
        :type bucket_names: List[str]
        """
        self.logger.info("Starting to process buckets for lifecycle policies.")
        for bucket_name in bucket_names:
            self.logger.info("Processing bucket: %s", bucket_name)
            rules = self.get_lifecycle_policy(bucket_name)
            if not rules:
                self.policies.append(
                    {"Bucket": bucket_name, **LifecyclePolicy.default_policy()}
                )
            else:
                for rule in rules:
                    analyzed_rule = LifecyclePolicy.from_rule(bucket_name, rule)
                    self.policies.append(analyzed_rule)
        self.logger.info("Finished processing buckets for lifecycle policies.")

    def save_policies_csv(self, filename: str) -> None:
        """
        Saves the extracted lifecycle policies to a CSV file.

        :param filename: Name of the CSV file where the data will be saved.
        :type filename: str
        """
        if not self.policies:
            self.logger.warning("No policies to save.")
            return

        try:
            fieldnames = [
                "Bucket",
                "Status",
                "ID",
                "Prefix",
                "Transitions",
                "ExpirationDays",
                "NoncurrentVersionTransitions",
                "NoncurrentVersionExpirationDays",
                "AbortIncompleteMultipartUploadDays",
            ]

            self.logger.info("Saving lifecycle policies to CSV file: %s", filename)
            with open(filename, mode="w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for policy in self.policies:
                    writer.writerow(policy)
            self.logger.info("Policies successfully saved to %s", filename)
        except IOError as error:
            self.logger.error("Error saving policies to file %s: %s", filename, error)
