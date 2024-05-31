# S3 Lifecycle Manager

The S3 Lifecycle Manager is a module designed to manage the lifecycle policies of S3 buckets. It allows you to process, export, and restore lifecycle policies, providing functionalities for backup and management of these policies.

**Versão em português disponível [aqui](README_pt_BR.md).**

## Author

- **Name:** Rodrigo de Souza Rampazzo
- **Email:** [rosorzz@protonmail.com](mailto:rosorzz@protonmail.com)
- **GitHub:** [rzz0](https://github.com/rzz0)

## Description

The S3 Lifecycle Manager is a powerful tool to manage the lifecycle policies of S3 buckets. S3 lifecycle policies help define rules for the transition and expiration of objects in S3, enabling storage optimization and cost reduction. This module facilitates the administration of these policies, offering functionalities to list, export, save, and restore lifecycle configurations.

### Key Features

- **List Buckets:** Lists all S3 buckets available in the AWS account.
- **Get Lifecycle Policies:** Retrieves lifecycle configurations for specified buckets.
- **Export Policies:** Exports lifecycle policies to JSON files, creating backups of the configurations.
- **Restore Policies:** Restores lifecycle policies from backup files.
- **Save Policies to CSV:** Saves lifecycle policies to a CSV file for analysis and documentation.

## Installation

To install the S3 Lifecycle Manager, you can use `pip`. First, make sure you have Python 3.6 or higher installed, then run the following command:

```bash
pip install s3_lifecycle_manager
```

Alternatively, you can clone the repository and install the package locally:

```bash
git clone https://github.com/rzz0/s3_lifecycle_manager.git
cd s3_lifecycle_manager
pip install .
```

## Usage

The main functionalities of the S3 Lifecycle Manager are accessible through the `s3_lifecycle_manager` command-line interface.

### Configuring AWS Credentials

Before running the S3 Lifecycle Manager, ensure your AWS credentials are configured. You can use the `configure_aws_credentials` function to prompt for credentials if they are not already set:

```python
from s3_lifecycle_manager.auth import configure_aws_credentials

configure_aws_credentials()
```

### Running the S3 Lifecycle Manager

To run the S3 Lifecycle Manager with backup functionality, use the following command:

```bash
s3_lifecycle_manager
```

This command will process all S3 buckets, save their lifecycle policies to a CSV file, and export the current lifecycle policies to backup files.

### Restoring Lifecycle Policies

To restore lifecycle policies from a backup file, you can use the `S3LifecycleBackupManager`:

```python
from s3_lifecycle_manager.backup_manager import S3LifecycleBackupManager

backup_manager = S3LifecycleBackupManager('./backups')
backup_manager.restore_lifecycle_policies('your-bucket-name')
```

## Project Structure

The project has the following structure:

- **`src/`**: Contains the source code for the S3 Lifecycle Manager.
- **`tests/`**: Contains the test cases for the project.
- **`README.md`**: This file.
- **`setup.py`**: Setup script for the package.
- **`pyproject.toml`**: Configuration file for the build system.

## Future Functionalities

Some of the features planned for future versions:

- **Support for Arguments (Args):** Will allow configuring parameters directly from the command line for greater flexibility and automation.
- **New Modules:**
  - **Detailed Reports:** Tools to generate detailed reports on the usage and effectiveness of lifecycle policies.
  - **Amazon S3 Storage Lens:** Features for configuring and obtaining information from Amazon S3 Storage Lens in conjunction with CloudWatch.
- **Integration with Other AWS Tools:** Improve integration with other AWS services, such as CloudWatch, for enhanced monitoring and logging.

If you have suggestions or specific features you would like to see in the S3 Lifecycle Manager, please open an issue in our GitHub repository.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

If you have any questions or feedback, feel free to reach out via email at [rosorzz@protonmail.com](mailto:rosorzz@protonmail.com).
