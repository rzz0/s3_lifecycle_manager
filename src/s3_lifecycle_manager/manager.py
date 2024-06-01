"""
S3 Lifecycle Manager
====================

This module manages the lifecycle policies of S3 buckets,
listing the buckets and extracting the lifecycle rules to save
in a CSV file. It includes information about buckets that do
not have lifecycle rules.

Example usage:
--------------
    from s3_lifecycle_manager import S3LifecycleManager

    manager = S3LifecycleManager()
    manager.process_buckets()
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
            else:
                self.logger.warning(
                    "Unable to get the lifecycle policy for bucket %s: %s",
                    bucket_name,
                    error,
                )
            return []

    def analyze_rule(self, rule: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes a lifecycle rule and extracts its information.

        :param rule: Lifecycle rule.
        :type rule: Dict[str, Any]
        :returns: Dictionary containing detailed information about the rule.
        :rtype: Dict[str, Any]
        """
        transitions = ", ".join(
            [
                f"{t.get('Days', 'N/A')} days to {t.get('StorageClass', 'N/A')}"
                for t in rule.get("Transitions", [])
            ]
        )
        expiration = rule.get("Expiration", {}).get("Days", "N/A")
        noncurrent_transitions = ", ".join(
            [
                f"{t.get('NoncurrentDays', 'N/A')} days to {t.get('StorageClass', 'N/A')}"
                for t in rule.get("NoncurrentVersionTransitions", [])
            ]
        )
        noncurrent_expiration = rule.get("NoncurrentVersionExpiration", {}).get(
            "NoncurrentDays", "N/A"
        )
        abort_multipart = rule.get("AbortIncompleteMultipartUpload", {}).get(
            "DaysAfterInitiation", "N/A"
        )

        filter_prefix = rule.get("Filter", {}).get("Prefix", "No Prefix")
        tag_filter = rule.get("Filter", {}).get("Tag", None)
        if tag_filter:
            filter_prefix += f", Tag: {tag_filter['Key']}={tag_filter['Value']}"

        return {
            "Status": rule.get("Status", "Unknown"),
            "ID": rule.get("ID", "No ID"),
            "Prefix": filter_prefix,
            "Transitions": transitions,
            "ExpirationDays": expiration,
            "NoncurrentVersionTransitions": noncurrent_transitions,
            "NoncurrentVersionExpirationDays": noncurrent_expiration,
            "AbortIncompleteMultipartUploadDays": abort_multipart,
        }

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
                    {
                        "Bucket": bucket_name,
                        "Status": "No Rules",
                        "ID": "N/A",
                        "Prefix": "N/A",
                        "Transitions": "N/A",
                        "ExpirationDays": "N/A",
                        "NoncurrentVersionTransitions": "N/A",
                        "NoncurrentVersionExpirationDays": "N/A",
                        "AbortIncompleteMultipartUploadDays": "N/A",
                    }
                )
            else:
                for rule in rules:
                    analyzed_rule = self.analyze_rule(rule)
                    analyzed_rule["Bucket"] = bucket_name
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

            self.logger.info(
                "Saving lifecycle policies to CSV file: %s", filename)
            with open(filename, mode="w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for policy in self.policies:
                    writer.writerow(policy)
            self.logger.info("Policies successfully saved to %s", filename)
        except IOError as error:
            self.logger.error(
                "Error saving policies to file %s: %s", filename, error)
