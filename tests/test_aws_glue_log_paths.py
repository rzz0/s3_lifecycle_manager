"""
Unit tests for the GlueLogPathsManager class.
"""

import unittest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from s3_lifecycle_manager.aws_glue_log_paths import GlueLogPathsManager


@patch("s3_lifecycle_manager.aws_glue_log_paths.boto3.client")
def test_list_glue_jobs_success(mock_boto_client):
    """
    Test listing Glue jobs successfully.
    """
    mock_glue_client = MagicMock()
    mock_boto_client.return_value = mock_glue_client

    manager = GlueLogPathsManager()

    mock_response = {
        "Jobs": [
            {"Name": "job1"},
            {"Name": "job2"},
        ]
    }
    mock_glue_client.get_jobs.return_value = mock_response

    jobs = manager.list_glue_jobs()

    assert len(jobs) == 2
    assert jobs[0]["Name"] == "job1"
    assert jobs[1]["Name"] == "job2"
    mock_glue_client.get_jobs.assert_called_once()


@patch("s3_lifecycle_manager.aws_glue_log_paths.boto3.client")
def test_list_glue_jobs_client_error(mock_boto_client):
    """
    Test handling a ClientError when listing Glue jobs.
    """
    mock_glue_client = MagicMock()
    mock_boto_client.return_value = mock_glue_client

    manager = GlueLogPathsManager()

    mock_glue_client.get_jobs.side_effect = ClientError(
        {"Error": {"Code": "500", "Message": "Internal Server Error"}}, "get_jobs"
    )

    jobs = manager.list_glue_jobs()

    assert jobs == []
    mock_glue_client.get_jobs.assert_called_once()


@patch("s3_lifecycle_manager.aws_glue_log_paths.boto3.client")
@patch("s3_lifecycle_manager.aws_glue_log_paths.csv.DictWriter")
@patch("builtins.open")
def test_save_report_csv_success(mock_open, mock_dict_writer, mock_boto_client):
    """
    Test saving the Glue jobs report to a CSV file successfully.
    """
    mock_glue_client = MagicMock()
    mock_boto_client.return_value = mock_glue_client

    manager = GlueLogPathsManager()
    manager.job_details = [
        {
            "JobName": "job1",
            "BucketName": "bucket1",
            "ContinuousLoggingEnabled": True,
            "TemporaryPath": "s3://temp_path1",
            "SparkUIEnabled": True,
            "SparkUILogsPath": "s3://spark_ui_path1",
        }
    ]

    mock_writer = MagicMock()
    mock_dict_writer.return_value = mock_writer

    manager.save_report_csv("test_report.csv")

    mock_open.assert_called_once_with(
        "test_report.csv", mode="w", encoding="utf-8", newline=""
    )
    mock_dict_writer.assert_called_once()
    mock_writer.writeheader.assert_called_once()
    mock_writer.writerows.assert_called_once_with(manager.job_details)


@patch("s3_lifecycle_manager.aws_glue_log_paths.boto3.client")
@patch("s3_lifecycle_manager.aws_glue_log_paths.csv.writer")
@patch("builtins.open")
def test_save_buckets_report_csv_success(mock_open, mock_writer, mock_boto_client):
    """
    Test saving the buckets report to a CSV file successfully.
    """
    mock_glue_client = MagicMock()
    mock_boto_client.return_value = mock_glue_client

    manager = GlueLogPathsManager()
    manager.buckets = {"bucket1", "bucket2"}

    mock_csv_writer = MagicMock()
    mock_writer.return_value = mock_csv_writer

    manager.save_buckets_report_csv("test_buckets_report.csv")

    mock_open.assert_called_once_with(
        "test_buckets_report.csv", mode="w", encoding="utf-8", newline=""
    )
    mock_writer.assert_called_once()
    calls = [
        unittest.mock.call(["BucketName"]),
        unittest.mock.call(["bucket1"]),
        unittest.mock.call(["bucket2"]),
    ]
    mock_csv_writer.writerow.assert_has_calls(calls, any_order=True)


@patch("s3_lifecycle_manager.aws_glue_log_paths.boto3.client")
def test_process_glue_jobs(mock_boto_client):
    """
    Test processing Glue jobs and extracting their log paths.
    """
    mock_glue_client = MagicMock()
    mock_boto_client.return_value = mock_glue_client

    manager = GlueLogPathsManager()

    mock_jobs = [
        {
            "Name": "job1",
            "Command": {"ScriptLocation": "s3://bucket1/scripts/script1.py"},
            "DefaultArguments": {
                "--enable-continuous-cloudwatch-log": "true",
                "--TempDir": "s3://temp_path1",
                "--enable-spark-ui": "true",
                "--spark-event-logs-path": "s3://spark_ui_path1",
            },
        }
    ]

    mock_glue_client.get_jobs.return_value = {"Jobs": mock_jobs}
    manager.process_glue_jobs()

    expected_job_details = {
        "JobName": "job1",
        "BucketName": "bucket1",
        "ContinuousLoggingEnabled": True,
        "TemporaryPath": "s3://temp_path1",
        "SparkUIEnabled": True,
        "SparkUILogsPath": "s3://spark_ui_path1",
    }
    assert len(manager.job_details) == 1
    assert manager.job_details[0] == expected_job_details
    assert "bucket1" in manager.buckets


if __name__ == "__main__":
    unittest.main()
