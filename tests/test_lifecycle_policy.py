import unittest
from s3_lifecycle_manager.lifecycle_policy import LifecyclePolicy


class TestLifecyclePolicy(unittest.TestCase):
    """Tests for the LifecyclePolicy class."""

    def test_default_policy(self):
        """Test the default lifecycle policy."""
        expected_policy = {
            "Status": "No Rules",
            "ID": "N/A",
            "Prefix": "N/A",
            "Transitions": "N/A",
            "ExpirationDays": "N/A",
            "NoncurrentVersionTransitions": "N/A",
            "NoncurrentVersionExpirationDays": "N/A",
            "AbortIncompleteMultipartUploadDays": "N/A",
        }
        self.assertEqual(LifecyclePolicy.default_policy(), expected_policy)

    def test_from_rule(self):
        """Test constructing a lifecycle policy from a rule."""
        rule = {
            "Status": "Enabled",
            "ID": "ExampleRule",
            "Filter": {"Prefix": "documents/"},
            "Transitions": [{"Days": 30, "StorageClass": "GLACIER"}],
            "Expiration": {"Days": 365},
            "NoncurrentVersionTransitions": [
                {"NoncurrentDays": 30, "StorageClass": "GLACIER"}
            ],
            "NoncurrentVersionExpiration": {"NoncurrentDays": 365},
            "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7},
        }
        expected_policy = {
            "Bucket": "example-bucket",
            "Status": "Enabled",
            "ID": "ExampleRule",
            "Prefix": "documents/",
            "Transitions": "30 days to GLACIER",
            "ExpirationDays": 365,
            "NoncurrentVersionTransitions": "30 days to GLACIER",
            "NoncurrentVersionExpirationDays": 365,
            "AbortIncompleteMultipartUploadDays": 7,
        }
        self.assertEqual(
            LifecyclePolicy.from_rule("example-bucket", rule), expected_policy
        )

    def test_from_rule_with_missing_fields(self):
        """Test constructing a lifecycle policy from a rule with missing optional fields."""
        rule = {
            "Status": "Enabled",
            "ID": "ExampleRule",
            "Filter": {"Prefix": ""},
            "Transitions": [],
            "Expiration": {},
            "NoncurrentVersionTransitions": [],
            "NoncurrentVersionExpiration": {},
            "AbortIncompleteMultipartUpload": {},
        }
        expected_policy = {
            "Bucket": "example-bucket",
            "Status": "Enabled",
            "ID": "ExampleRule",
            "Prefix": "No Prefix",
            "Transitions": "N/A",
            "ExpirationDays": "N/A",
            "NoncurrentVersionTransitions": "N/A",
            "NoncurrentVersionExpirationDays": "N/A",
            "AbortIncompleteMultipartUploadDays": "N/A",
        }
        self.assertEqual(
            LifecyclePolicy.from_rule("example-bucket", rule), expected_policy
        )

    def test_from_rule_with_tag_filter(self):
        """Test constructing a lifecycle policy from a rule with a tag filter."""
        rule = {
            "Status": "Enabled",
            "ID": "ExampleRule",
            "Filter": {"Tag": {"Key": "Environment", "Value": "Production"}},
            "Transitions": [{"Days": 30, "StorageClass": "GLACIER"}],
            "Expiration": {"Days": 365},
        }
        expected_policy = {
            "Bucket": "example-bucket",
            "Status": "Enabled",
            "ID": "ExampleRule",
            "Prefix": "No Prefix, Tag: Environment=Production",
            "Transitions": "30 days to GLACIER",
            "ExpirationDays": 365,
            "NoncurrentVersionTransitions": "N/A",
            "NoncurrentVersionExpirationDays": "N/A",
            "AbortIncompleteMultipartUploadDays": "N/A",
        }
        self.assertEqual(
            LifecyclePolicy.from_rule("example-bucket", rule), expected_policy
        )


if __name__ == "__main__":
    unittest.main()
