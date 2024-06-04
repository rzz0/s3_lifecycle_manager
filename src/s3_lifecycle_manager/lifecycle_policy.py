"""
Lifecycle Policy Management
============================

This module provides a class for managing the lifecycle policies of S3 buckets.
It includes methods for returning a default policy and for constructing a lifecycle
policy dictionary from a given rule.

Example usage:
--------------
    from s3_lifecycle_manager.lifecycle_policy import LifecyclePolicy

    # Get the default lifecycle policy
    default_policy = LifecyclePolicy.default_policy()

    # Construct a lifecycle policy from a rule
    rule = {
        "Status": "Enabled",
        "ID": "ExampleRule",
        "Filter": {"Prefix": "documents/"},
        "Transitions": [{"Days": 30, "StorageClass": "GLACIER"}],
        "Expiration": {"Days": 365}
    }
    policy = LifecyclePolicy.from_rule("example-bucket", rule)

Dependencies:
-------------
- typing

Author:
-------
- Rodrigo de Souza Rampazzo <rosorzz@protonmail.com>
- GitHub: https://github.com/rzz0

License:
--------
MIT License
"""

from typing import Dict, Any


class LifecyclePolicy:
    """
    A class to manage the lifecycle policies of S3 buckets.

    Provides methods to get the default lifecycle policy and to construct
    a lifecycle policy dictionary from a given rule.
    """

    @staticmethod
    def default_policy() -> Dict[str, Any]:
        """
        Returns the default lifecycle policy.

        The default policy indicates that there are no rules configured
        for the bucket.

        :returns: A dictionary representing the default lifecycle policy.
        :rtype: Dict[str, Any]
        """
        return {
            "Status": "No Rules",
            "ID": "N/A",
            "Prefix": "N/A",
            "Transitions": "N/A",
            "ExpirationDays": "N/A",
            "NoncurrentVersionTransitions": "N/A",
            "NoncurrentVersionExpirationDays": "N/A",
            "AbortIncompleteMultipartUploadDays": "N/A",
        }

    @staticmethod
    def from_rule(bucket_name: str, rule: Dict[str, Any]) -> Dict[str, Any]:
        """
        Constructs a lifecycle policy dictionary from a given rule.

        This method extracts and formats the details of a lifecycle rule
        into a dictionary that includes information such as status, ID,
        filter prefix, transitions, expiration days, and other attributes.

        :param bucket_name: The name of the S3 bucket to which the rule applies.
        :type bucket_name: str
        :param rule: The lifecycle rule to be converted into a policy dictionary.
        :type rule: Dict[str, Any]
        :returns: A dictionary representing the lifecycle policy based on the rule.
        :rtype: Dict[str, Any]
        """
        transitions = (
            ", ".join(
                [
                    f"{t.get('Days', 'N/A')} days to {t.get('StorageClass', 'N/A')}"
                    for t in rule.get("Transitions", [])
                ]
            )
            or "N/A"
        )
        expiration = rule.get("Expiration", {}).get("Days", "N/A")
        noncurrent_transitions = (
            ", ".join(
                [
                    f"{t.get('NoncurrentDays', 'N/A')} days to {t.get('StorageClass', 'N/A')}"
                    for t in rule.get("NoncurrentVersionTransitions", [])
                ]
            )
            or "N/A"
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
        filter_prefix = filter_prefix or "No Prefix"

        return {
            "Bucket": bucket_name,
            "Status": rule.get("Status", "Unknown"),
            "ID": rule.get("ID", "No ID"),
            "Prefix": filter_prefix,
            "Transitions": transitions,
            "ExpirationDays": expiration,
            "NoncurrentVersionTransitions": noncurrent_transitions,
            "NoncurrentVersionExpirationDays": noncurrent_expiration,
            "AbortIncompleteMultipartUploadDays": abort_multipart,
        }
