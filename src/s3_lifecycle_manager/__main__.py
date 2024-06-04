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

import argparse
from botocore.exceptions import ClientError
from s3_lifecycle_manager.manager import S3LifecycleManager
from s3_lifecycle_manager.backup_manager import S3LifecycleBackupManager
from s3_lifecycle_manager.aws_glue_log_paths import GlueLogPathsManager
from s3_lifecycle_manager.logger import configure_logging, get_logger


def main():
    """
    Main function to run the S3 bucket lifecycle manager with
    backup functionality.
    """
    parser = argparse.ArgumentParser(description="S3 Lifecycle Manager Script")
    parser.add_argument("--logs", action="store_true", help="Process AWS Glue job logs")
    args = parser.parse_args()

    configure_logging()
    logger = get_logger(__name__)

    logger.info("Starting the S3 bucket lifecycle manager script.")
    logger.info("process_glue_logs flag is set to: %s", args.logs)

    backup_dir = "./backups"
    manager = S3LifecycleManager()
    backup_manager = S3LifecycleBackupManager(backup_dir)
    glue_log_manager = GlueLogPathsManager()

    if args.logs:
        logger.info("Process Glue logs is enabled. Starting Glue log processing.")
        glue_log_manager.process_glue_jobs()

        logger.info("Saving Glue jobs log paths report to CSV.")
        glue_log_manager.save_report_csv("REPORT_glue_jobs_report.csv")

        logger.info("Saving Glue jobs buckets report to CSV.")
        glue_log_manager.save_buckets_report_csv("REPORT_glue_jobs_buckets_report.csv")
    else:
        try:
            logger.info("Listing all S3 buckets.")
            bucket_names = [bucket["Name"] for bucket in manager.list_buckets()]

            logger.info("Processing S3 buckets to extract lifecycle policies.")
            manager.process_buckets(bucket_names)

            logger.info("Saving lifecycle policies to CSV.")
            manager.save_policies_csv("REPORT_lifecycle_buckets.csv")

            logger.info("Exporting current lifecycle policies.")
            lifecycle_policies = {
                policy["Bucket"]: manager.get_lifecycle_policy(policy["Bucket"])
                for policy in manager.policies
            }
            backup_manager.export_lifecycle_policies(lifecycle_policies)

            logger.info("Finished the S3 bucket lifecycle manager script.")
        except ClientError as error:
            logger.error("An AWS client error occurred: %s", error)
        except Exception as error:  # pylint: disable=W0718
            logger.error("An unexpected error occurred: %s", error)


if __name__ == "__main__":
    main()
