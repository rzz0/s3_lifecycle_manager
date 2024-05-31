from setuptools import setup, find_packages

setup(
    name="s3_lifecycle_manager",
    version="0.1.0",
    description="A module to manage the lifecycle policies of S3 buckets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rodrigo de Souza Rampazzo",
    author_email="rosorzz@protonmail.com",
    url="https://github.com/rzz0/s3_lifecycle_manager",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=["boto3", "botocore"],
    entry_points={
        "console_scripts": [
            "s3_lifecycle_manager=s3_lifecycle_manager.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="aws s3 lifecycle management boto3",
)
