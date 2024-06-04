"""
AWS Glue Log Paths Manager
==========================

This module lists all temporary paths and Spark UI logs paths of all AWS Glue jobs in the account.
It generates a report in CSV format containing the bucket name, if continuous logging is enabled,
the temporary path, if Spark UI is enabled, and the Spark UI logs path.

Example usage:
--------------
    from aws_glue_log_paths import GlueLogPathsManager

    manager = GlueLogPathsManager()
    manager.process_glue_jobs()
    manager.save_report_csv('glue_jobs_report.csv')
    manager.save_buckets_report_csv('glue_jobs_buckets_report.csv')

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
import boto3
from botocore.exceptions import ClientError
from .logger import get_logger

DEFAULT_TEMP_PATH = "N/A"
DEFAULT_FALSE = "false"


class GlueLogPathsManager:
    """
    A class to manage AWS Glue job log paths.
    """

    def __init__(self):
        self.glue_client = boto3.client("glue")
        self.logger = get_logger(__name__)
        self.job_details = []
        self.buckets = set()

    def list_glue_jobs(self):
        """
        Lists all AWS Glue jobs.
        """
        try:
            response = self.glue_client.get_jobs()
            jobs = response.get("Jobs", [])
            self.logger.info("Found %d Glue jobs.", len(jobs))
            return jobs
        except ClientError as error:
            self.logger.error("Error listing Glue jobs: %s", error)
            return []

    def process_glue_jobs(self):
        """
        Processes all Glue jobs and extracts their log paths.
        """
        self.logger.info("Starting to process Glue jobs for log paths.")
        jobs = self.list_glue_jobs()
        for job in jobs:
            job_name = job["Name"]
            self.logger.info("Processing job: %s", job_name)
            bucket_name = job.get("Command", {}).get("ScriptLocation", "").split("/")[2]

            default_arguments = job.get("DefaultArguments", {})
            continuous_log = (
                default_arguments.get(
                    "--enable-continuous-cloudwatch-log", DEFAULT_FALSE
                )
                == "true"
            )
            temp_path = default_arguments.get("--TempDir", DEFAULT_TEMP_PATH)
            spark_ui_enabled = (
                default_arguments.get("--enable-spark-ui", DEFAULT_FALSE) == "true"
            )
            spark_ui_path = default_arguments.get(
                "--spark-event-logs-path", DEFAULT_TEMP_PATH
            )

            self.logger.info(
                "Job: %s, TempDir: %s, Continuous Log: %s, Spark UI Enabled: %s, Spark UI Path: %s",
                job_name,
                temp_path,
                continuous_log,
                spark_ui_enabled,
                spark_ui_path,
            )

            self.job_details.append(
                {
                    "JobName": job_name,
                    "BucketName": bucket_name,
                    "ContinuousLoggingEnabled": continuous_log,
                    "TemporaryPath": temp_path,
                    "SparkUIEnabled": spark_ui_enabled,
                    "SparkUILogsPath": spark_ui_path,
                }
            )
            self.buckets.add(bucket_name)
        self.logger.info("Finished processing Glue jobs for log paths.")

    def save_report_csv(self, filename):
        """
        Saves the Glue jobs log paths report to a CSV file.

        :param filename: Name of the CSV file where the data will be saved.
        :type filename: str
        """
        if not self.job_details:
            self.logger.warning("No Glue job details to save.")
            return

        try:
            fieldnames = [
                "JobName",
                "BucketName",
                "ContinuousLoggingEnabled",
                "TemporaryPath",
                "SparkUIEnabled",
                "SparkUILogsPath",
            ]
            self.logger.info(
                "Saving Glue jobs log paths report to CSV file: %s", filename
            )
            with open(filename, mode="w", encoding="utf-8", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.job_details)
            self.logger.info(
                "Glue jobs log paths report successfully saved to %s", filename
            )
        except OSError as error:
            self.logger.error(
                "Error saving Glue jobs log paths report to file %s: %s",
                filename,
                error,
            )

    def save_buckets_report_csv(self, filename):
        """
        Saves the report of buckets used in Glue jobs to a CSV file.

        :param filename: Name of the CSV file where the data will be saved.
        :type filename: str
        """
        if not self.buckets:
            self.logger.warning("No buckets to save.")
            return

        try:
            self.logger.info(
                "Saving Glue jobs buckets report to CSV file: %s", filename
            )
            with open(filename, mode="w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["BucketName"])
                for bucket in self.buckets:
                    writer.writerow([bucket])
            self.logger.info(
                "Glue jobs buckets report successfully saved to %s", filename
            )
        except OSError as error:
            self.logger.error(
                "Error saving Glue jobs buckets report to file %s: %s", filename, error
            )


if __name__ == "__main__":
    manager = GlueLogPathsManager()
    manager.process_glue_jobs()
    manager.save_report_csv("REPORT_glue_jobs_log_path_report.csv")
    manager.save_buckets_report_csv("REPORT_glue_jobs_buckets_report.csv")
