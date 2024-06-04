# S3 Lifecycle Manager

The S3 Lifecycle Manager is a module designed to manage the lifecycle policies of S3 buckets. It allows you to process, export, and restore lifecycle policies, providing functionalities for backup and management of these policies.

**Versão em português disponível [aqui](README_pt_BR.md).**

## Author

- **Name:** Rodrigo de Souza Rampazzo
- **Email:** [rosorzz@protonmail.com](mailto:rosorzz@protonmail.com)
- **GitHub:** [rzz0](https://github.com/rzz0)

## Description

The S3 Lifecycle Manager is a Python package designed to manage the lifecycle policies of S3 buckets. S3 lifecycle policies help define rules for the transition and expiration of objects in S3, enabling storage optimization and cost reduction. This module facilitates the administration of these policies, offering functionalities to list, export, save, and restore lifecycle configurations.

### Key Features

- **List Buckets:** Retrieves and lists all S3 buckets in your AWS account.
- **Extract Lifecycle Policies:** Extracts lifecycle policies for each bucket and saves them to a CSV file.
- **Backup Policies:** Exports lifecycle policies to a specified directory.
- **Restore Policies:** Restores lifecycle policies from backups.
- **AWS Glue Log Paths:** Lists all temporary paths and Spark UI logs paths of AWS Glue jobs and generates reports.

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

### Running the S3 Lifecycle Manager

To run the S3 Lifecycle Manager with backup functionality, use the following command:

```bash
s3_lifecycle_manager
```

This command will process all S3 buckets, save their lifecycle policies to a CSV file, and export the current lifecycle policies to backup files.

### S3 Lifecycle Manager Help

Show options to S3 Lifecycle Manager:

```bash
s3_lifecycle_manager -h
```

This command will show all options to S3 Lifecycle Manager.

### Restoring Lifecycle Policies

To restore lifecycle policies from a backup file, you can use the `S3LifecycleBackupManager`:

```python
s3_lifecycle_manager --restore --bucket bucket-name-to-restore
```

## AWS Glue Log Paths

### Command Line Usage

You can also use the module from the command line:

```
s3_lifecycle_manager --logs-glue-job
```

## Development

### Setting Up

Set up a virtual environment and install dependencies using the `Makefile`:

```bash
make
```

### Running Tests

To run tests:

```bash
make test
```

### Cleaning Up

To clean up the environment:

```bash
make clean
```

### Formatting Code

To format the code:

```bash
make format
```

### Linting

To run static code analysis:

```bash
make lint
```

### Security Check

To run security checks:

```bash
make security
```

### Updating Dependencies

To update dependencies:

```bash
make update
```

## Project Structure

The project has the following structure:

- **`src/`**: Contains the source code for the S3 Lifecycle Manager.
- **`tests/`**: Contains the test cases for the project.
- **`README.md`**: This file.
- **`LICENSE`**: MIT License.
- **`setup.py`**: Setup script for the package.
- **`pyproject.toml`**: Configuration file for the build system.
- **`Makefile`**: Set up a virtual environment and install dependencies.
- **`pytest.ini`**: Set up src dir to pytest.

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
