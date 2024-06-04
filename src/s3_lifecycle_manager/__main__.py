"""
S3 Lifecycle Manager
====================

This module manages the lifecycle policies of S3 buckets, listing the buckets
and extracting the lifecycle rules to save in a CSV file. It includes
information about buckets that do not have lifecycle rules. Additionally,
it provides functionality to back up and optionally restore lifecycle policies.

Example usage:
--------------
    # Process AWS Glue job logs and save reports
    python s3_lifecycle_manager.py --logs-glue-job

    # Restore lifecycle policies from backup for a specific bucket
    python s3_lifecycle_manager.py --restore --bucket example-bucket

    # Default usage: List buckets, process lifecycle policies, save to CSV, and export policies
    python s3_lifecycle_manager.py

Dependencies:
-------------
- boto3

Author:
-------
- Rodrigo de Souza Rampazzo <rosorzz@protonmail.com>
- GitHub: https://github.com/rzz0/s3_lifecycle_manager

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

REPORT_LIFECYCLE_BUCKETS_CSV = "REPORT_lifecycle_buckets.csv"
REPORT_GLUE_JOBS_REPORT_CSV = "REPORT_glue_jobs_report.csv"
REPORT_GLUE_JOBS_BUCKETS_REPORT_CSV = "REPORT_glue_jobs_buckets_report.csv"


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="S3 Lifecycle Manager Script")
    parser.add_argument(
        "--logs-glue-job",
        action="store_true",
        help="Process AWS Glue job logs and save the log paths and buckets report to CSV files.",
    )
    parser.add_argument(
        "--restore",
        action="store_true",
        help="Restore lifecycle policies from backup files.",
    )
    parser.add_argument(
        "--bucket",
        type=str,
        help="Specify the bucket name to restore the lifecycle policy from a backup file.",
    )
    return parser.parse_args()


def process_glue_logs(glue_log_manager):
    """
    Process AWS Glue job logs and save reports.

    :param glue_log_manager: Instance of GlueLogPathsManager
    """
    glue_log_manager.process_glue_jobs()
    glue_log_manager.save_report_csv(REPORT_GLUE_JOBS_REPORT_CSV)
    glue_log_manager.save_buckets_report_csv(REPORT_GLUE_JOBS_BUCKETS_REPORT_CSV)


def restore_lifecycle_policies(backup_manager, bucket):
    """
    Restore lifecycle policies for a specific bucket from backup.

    :param backup_manager: Instance of S3LifecycleBackupManager
    :param bucket: Name of the bucket to restore policies for
    """
    backup_manager.restore_lifecycle_policies(bucket)


def process_and_save_lifecycle_policies(manager, backup_manager):
    """
    Process S3 buckets to extract lifecycle policies and save them to CSV.

    :param manager: Instance of S3LifecycleManager
    :param backup_manager: Instance of S3LifecycleBackupManager
    """
    bucket_names = [bucket["Name"] for bucket in manager.list_buckets()]
    manager.process_buckets(bucket_names)
    manager.save_policies_csv(REPORT_LIFECYCLE_BUCKETS_CSV)
    lifecycle_policies = {
        policy["Bucket"]: manager.get_lifecycle_policy(policy["Bucket"])
        for policy in manager.policies
    }
    backup_manager.export_lifecycle_policies(lifecycle_policies)


def main():
    """Main function to run the S3 bucket lifecycle manager with backup functionality."""
    args = parse_arguments()

    configure_logging()
    logger = get_logger(__name__)

    logger.info("Starting the S3 bucket lifecycle manager script.")
    logger.info("Process Glue logs flag is set to: %s", args.logs_glue_job)
    logger.info("Restore flag is set to: %s", args.restore)
    logger.info("Bucket to restore is set to: %s", args.bucket)

    backup_dir = "./backups"
    manager = S3LifecycleManager()
    backup_manager = S3LifecycleBackupManager(backup_dir)
    glue_log_manager = GlueLogPathsManager()

    if args.logs_glue_job:
        logger.info("Process Glue logs is enabled. Starting Glue log processing.")
        process_glue_logs(glue_log_manager)
    elif args.restore:
        if not args.bucket:
            logger.error("Bucket name is required for restoring lifecycle policies.")
            return
        try:
            logger.info("Restoring lifecycle policies for bucket: %s", args.bucket)
            restore_lifecycle_policies(backup_manager, args.bucket)
            logger.info(
                "Successfully restored lifecycle policies for bucket: %s", args.bucket
            )
        except ClientError as error:
            logger.error("An AWS client error occurred while restoring: %s", error)
        except Exception as error:  # pylint: disable=W0718
            logger.error("An unexpected error occurred while restoring: %s", error)
    else:
        try:
            logger.info("Listing all S3 buckets.")
            process_and_save_lifecycle_policies(manager, backup_manager)
            logger.info("Finished the S3 bucket lifecycle manager script.")
        except ClientError as error:
            logger.error("An AWS client error occurred: %s", error)
        except Exception as error:  # pylint: disable=W0718
            logger.error("An unexpected error occurred: %s", error)


if __name__ == "__main__":
    main()
