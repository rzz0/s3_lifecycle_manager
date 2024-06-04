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


def main():
    """
    Main function to run the S3 bucket lifecycle manager with
    backup functionality.
    """
    parser = argparse.ArgumentParser(description="S3 Lifecycle Manager Script")
    parser.add_argument("--logs-glue-job", action="store_true",
                        help="Process AWS Glue job logs and save the log paths and buckets report to CSV files.")
    parser.add_argument("--restore", action="store_true",
                        help="Restore lifecycle policies from backup files.")
    parser.add_argument(
        "--bucket", type=str, help="Specify the bucket name to restore the lifecycle policy from a backup file.")
    args = parser.parse_args()

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
        logger.info(
            "Process Glue logs is enabled. Starting Glue log processing.")
        glue_log_manager.process_glue_jobs()

        logger.info("Saving Glue jobs log paths report to CSV.")
        glue_log_manager.save_report_csv("REPORT_glue_jobs_report.csv")

        logger.info("Saving Glue jobs buckets report to CSV.")
        glue_log_manager.save_buckets_report_csv(
            "REPORT_glue_jobs_buckets_report.csv")
    elif args.restore:
        if not args.bucket:
            logger.error(
                "Bucket name is required for restoring lifecycle policies.")
            return

        try:
            logger.info(
                "Restoring lifecycle policies for bucket: %s", args.bucket)
            backup_manager.restore_lifecycle_policies(args.bucket)
            logger.info(
                "Successfully restored lifecycle policies for bucket: %s", args.bucket)
        except ClientError as error:
            logger.error(
                "An AWS client error occurred while restoring: %s", error)
        except Exception as error:  # pylint: disable=W0718
            logger.error(
                "An unexpected error occurred while restoring: %s", error)
    else:
        try:
            logger.info("Listing all S3 buckets.")
            bucket_names = [bucket["Name"]
                            for bucket in manager.list_buckets()]

            logger.info("Processing S3 buckets to extract lifecycle policies.")
            manager.process_buckets(bucket_names)

            logger.info("Saving lifecycle policies to CSV.")
            manager.save_policies_csv("REPORT_lifecycle_buckets.csv")

            logger.info("Exporting current lifecycle policies.")
            lifecycle_policies = {
                policy["Bucket"]: manager.get_lifecycle_policy(
                    policy["Bucket"])
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
