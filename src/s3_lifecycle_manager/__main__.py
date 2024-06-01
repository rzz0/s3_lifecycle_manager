"""
S3 Lifecycle Manager
====================

This module manages the lifecycle policies of S3 buckets, listing the buckets
and extracting the lifecycle rules to save in a CSV file. It includes
information about buckets that do not have lifecycle rules. Additionally,
it provides functionality to back up and optionally restore lifecycle policies.

Example usage:
--------------
    from s3_lifecycle_manager import S3LifecycleManager, S3LifecycleBackupManager

    manager = S3LifecycleManager()
    manager.process_buckets()
    manager.save_policies_csv('lifecycle_buckets.csv')

    backup_manager = S3LifecycleBackupManager('./backups')
    backup_manager.export_lifecycle_policies(manager.list_buckets())

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

from botocore.exceptions import ClientError
from .manager import S3LifecycleManager
from .backup_manager import S3LifecycleBackupManager
from .logger import configure_logging, get_logger


def main():
    """
    Main function to run the S3 bucket lifecycle manager with
    backup functionality.
    """
    configure_logging()
    logger = get_logger(__name__)

    logger.info("Starting the S3 bucket lifecycle manager script.")

    # Directory where backups will be stored
    backup_dir = "./backups"
    manager = S3LifecycleManager()
    backup_manager = S3LifecycleBackupManager(backup_dir)

    try:
        # Process buckets and generate backup of lifecycle policies
        logger.info("Listing all S3 buckets.")
        bucket_names = [bucket["Name"] for bucket in manager.list_buckets()]

        logger.info("Processing S3 buckets to extract lifecycle policies.")
        manager.process_buckets(bucket_names)

        logger.info("Saving lifecycle policies to CSV.")
        manager.save_policies_csv("lifecycle_buckets.csv")

        logger.info("Exporting current lifecycle policies.")
        lifecycle_policies = {policy['Bucket']: manager.get_lifecycle_policy(
            policy['Bucket']) for policy in manager.policies}
        backup_manager.export_lifecycle_policies(lifecycle_policies)

        # Optional: Restore lifecycle policies for a specific bucket
        # backup_manager.restore_lifecycle_policies('bucket-name')

        logger.info("Finished the S3 bucket lifecycle manager script.")
    except ClientError as error:
        logger.error("An AWS client error occurred: %s", error)
    except Exception as error:  # pylint: disable=W0718
        logger.error("An unexpected error occurred: %s", error)


if __name__ == "__main__":
    main()
