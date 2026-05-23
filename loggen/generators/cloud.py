"""Cloud audit log generator (AWS CloudTrail style)."""

import random
from typing import List

from loggen.models.log_event import LogEvent, LogLevel
from .base import BaseGenerator


class CloudGenerator(BaseGenerator):
    """Generate cloud audit logs (AWS CloudTrail / Azure activity log style)."""

    SCENARIOS = {
        "console_login": "Cloud console login attempts (success/fail)",
        "iam_changes": "IAM policy/user/role modifications",
        "bucket_access": "S3/blob storage access (read/delete/public)",
        "key_creation": "Access key creation and rotation",
        "suspicious_api": "Unusual API call patterns",
        "resource_changes": "Compute/network resource changes",
    }

    AWS_REGIONS = [
        "us-east-1",
        "us-east-2",
        "us-west-1",
        "us-west-2",
        "eu-west-1",
        "eu-central-1",
        "ap-southeast-1",
        "ap-northeast-1",
    ]

    IAM_ACTIONS = [
        "CreateUser",
        "DeleteUser",
        "AttachUserPolicy",
        "DetachUserPolicy",
        "CreateRole",
        "DeleteRole",
        "PutRolePolicy",
        "CreateAccessKey",
        "DeleteAccessKey",
        "UpdateAccessKey",
    ]

    S3_ACTIONS = [
        "GetObject",
        "PutObject",
        "DeleteObject",
        "ListBucket",
        "PutBucketPolicy",
        "PutBucketAcl",
        "DeleteBucket",
    ]

    SUSPICIOUS_APIS = [
        "GetCallerIdentity",
        "ListUsers",
        "ListRoles",
        "GetAccountSummary",
        "DescribeInstances",
        "DescribeSecurityGroups",
        "ListBuckets",
    ]

    def generate(self, count: int = 10, scenario: str = "console_login", **kwargs) -> List[LogEvent]:
        """Generate cloud audit logs based on scenario."""
        if scenario == "console_login":
            return self._generate_console_login(count)
        elif scenario == "iam_changes":
            return self._generate_iam_changes(count)
        elif scenario == "bucket_access":
            return self._generate_bucket_access(count)
        elif scenario == "key_creation":
            return self._generate_key_creation(count)
        elif scenario == "suspicious_api":
            return self._generate_suspicious_api(count)
        elif scenario == "resource_changes":
            return self._generate_resource_changes(count)
        else:
            return self._generate_console_login(count)

    def _generate_console_login(self, count: int) -> List[LogEvent]:
        """Generate cloud console login logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=30, max_seconds=600)

            user = self.faker.username()
            src_ip = self.faker.ipv4()
            region = random.choice(self.AWS_REGIONS)
            success = not self._should_be_malicious()
            mfa_used = random.choice([True, False])

            result = "Success" if success else "Failure"
            mfa_status = "MFA used" if mfa_used else "MFA not used"

            message = f"Console Login {result}: User {user} from {src_ip} ({region}, {mfa_status})"

            level = LogLevel.INFO if success and mfa_used else LogLevel.WARNING

            event = LogEvent(
                timestamp=timestamp,
                source="cloud",
                event_type="console_login",
                level=level,
                message=message,
                fields={
                    "user_identity": user,
                    "src_ip": src_ip,
                    "aws_region": region,
                    "event_name": "ConsoleLogin",
                    "result": result,
                    "mfa_used": mfa_used,
                    "user_agent": self.faker.user_agent(),
                    "account_id": str(random.randint(100000000000, 999999999999)),
                    "user_type": random.choice(["IAMUser", "AssumedRole", "Root"]),
                },
            )
            events.append(event)

        return events

    def _generate_iam_changes(self, count: int) -> List[LogEvent]:
        """Generate IAM modification logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=60, max_seconds=1800)

            user = self.faker.username()
            target_user = self.faker.username()
            action = random.choice(self.IAM_ACTIONS)
            src_ip = self.faker.ipv4()
            region = random.choice(self.AWS_REGIONS)

            message = f"IAM Change: {user} performed {action} on {target_user} from {src_ip}"

            # Critical actions get higher severity
            critical_actions = ["AttachUserPolicy", "CreateAccessKey", "PutRolePolicy"]
            level = LogLevel.WARNING if action in critical_actions else LogLevel.INFO

            event = LogEvent(
                timestamp=timestamp,
                source="cloud",
                event_type="iam_modification",
                level=level,
                message=message,
                fields={
                    "user_identity": user,
                    "target_resource": target_user,
                    "src_ip": src_ip,
                    "aws_region": region,
                    "event_name": action,
                    "event_source": "iam.amazonaws.com",
                    "request_id": self._generate_request_id(),
                    "user_agent": "aws-cli/2.x",
                    "policy_name": (
                        f"AdminPolicy-{random.randint(1000, 9999)}"
                        if "Policy" in action
                        else None
                    ),
                },
            )
            events.append(event)

        return events

    def _generate_bucket_access(self, count: int) -> List[LogEvent]:
        """Generate S3 bucket access logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=5, max_seconds=60)

            user = self.faker.username()
            bucket = f"prod-{random.choice(['data', 'backups', 'logs', 'media'])}-{random.randint(1000, 9999)}"
            action = random.choice(self.S3_ACTIONS)
            src_ip = self.faker.ipv4()
            object_key = f"data/{self.faker.fake.file_name()}"

            # Public access or deletes are more suspicious
            is_suspicious = action in ["PutBucketPolicy", "PutBucketAcl", "DeleteBucket"]
            level = LogLevel.WARNING if is_suspicious else LogLevel.INFO

            message = f"S3 Access: {user} {action} on bucket {bucket}/{object_key}"

            event = LogEvent(
                timestamp=timestamp,
                source="cloud",
                event_type="s3_access",
                level=level,
                message=message,
                fields={
                    "user_identity": user,
                    "src_ip": src_ip,
                    "event_name": action,
                    "event_source": "s3.amazonaws.com",
                    "bucket_name": bucket,
                    "object_key": object_key,
                    "bytes_transferred": random.randint(0, 10000000),
                    "request_id": self._generate_request_id(),
                    "is_public": is_suspicious,
                },
            )
            events.append(event)

        return events

    def _generate_key_creation(self, count: int) -> List[LogEvent]:
        """Generate access key creation logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=120, max_seconds=3600)

            user = self.faker.username()
            src_ip = self.faker.ipv4()
            access_key_id = f"AKIA{self._random_alpha_upper(16)}"
            region = random.choice(self.AWS_REGIONS)

            message = f"Access key created for {user}: {access_key_id[:8]}... from {src_ip}"

            event = LogEvent(
                timestamp=timestamp,
                source="cloud",
                event_type="access_key_created",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "user_identity": user,
                    "src_ip": src_ip,
                    "aws_region": region,
                    "event_name": "CreateAccessKey",
                    "event_source": "iam.amazonaws.com",
                    "access_key_id": access_key_id,
                    "request_id": self._generate_request_id(),
                    "user_agent": "aws-cli/2.x",
                },
            )
            events.append(event)

        return events

    def _generate_suspicious_api(self, count: int) -> List[LogEvent]:
        """Generate suspicious API call patterns (reconnaissance)."""
        events = []

        user = self.faker.username()
        src_ip = self.faker.ipv4()

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=1, max_seconds=5)

            api_call = random.choice(self.SUSPICIOUS_APIS)
            region = random.choice(self.AWS_REGIONS)

            message = f"Reconnaissance API call: {user} called {api_call} from {src_ip}"

            event = LogEvent(
                timestamp=timestamp,
                source="cloud",
                event_type="reconnaissance",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "user_identity": user,
                    "src_ip": src_ip,
                    "aws_region": region,
                    "event_name": api_call,
                    "event_source": self._api_source(api_call),
                    "request_id": self._generate_request_id(),
                    "user_agent": "aws-cli/2.x",
                    "pattern": "discovery",
                    "api_calls_per_minute": random.randint(20, 100),
                },
            )
            events.append(event)

        return events

    def _generate_resource_changes(self, count: int) -> List[LogEvent]:
        """Generate compute/network resource change logs."""
        events = []

        actions = [
            ("RunInstances", "ec2.amazonaws.com"),
            ("TerminateInstances", "ec2.amazonaws.com"),
            ("AuthorizeSecurityGroupIngress", "ec2.amazonaws.com"),
            ("CreateSecurityGroup", "ec2.amazonaws.com"),
            ("DeleteSecurityGroup", "ec2.amazonaws.com"),
        ]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=60, max_seconds=1800)

            user = self.faker.username()
            src_ip = self.faker.ipv4()
            action, source = random.choice(actions)
            region = random.choice(self.AWS_REGIONS)
            resource_id = f"i-{self._random_alpha_lower(17)}"

            message = f"Resource Change: {user} performed {action} on {resource_id} from {src_ip}"

            critical = "Authorize" in action or "Terminate" in action
            level = LogLevel.WARNING if critical else LogLevel.INFO

            event = LogEvent(
                timestamp=timestamp,
                source="cloud",
                event_type="resource_change",
                level=level,
                message=message,
                fields={
                    "user_identity": user,
                    "src_ip": src_ip,
                    "aws_region": region,
                    "event_name": action,
                    "event_source": source,
                    "resource_id": resource_id,
                    "request_id": self._generate_request_id(),
                },
            )
            events.append(event)

        return events

    @staticmethod
    def _api_source(api_call: str) -> str:
        """Map API call to source service."""
        mapping = {
            "GetCallerIdentity": "sts.amazonaws.com",
            "ListUsers": "iam.amazonaws.com",
            "ListRoles": "iam.amazonaws.com",
            "GetAccountSummary": "iam.amazonaws.com",
            "DescribeInstances": "ec2.amazonaws.com",
            "DescribeSecurityGroups": "ec2.amazonaws.com",
            "ListBuckets": "s3.amazonaws.com",
        }
        return mapping.get(api_call, "unknown")

    @staticmethod
    def _generate_request_id() -> str:
        """Generate a CloudTrail request ID."""
        return f"{random.randint(10**11, 10**12 - 1):012x}-{random.randint(1000, 9999)}"

    @staticmethod
    def _random_alpha_upper(length: int) -> str:
        """Generate uppercase alphanumeric."""
        import string

        return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

    @staticmethod
    def _random_alpha_lower(length: int) -> str:
        """Generate lowercase alphanumeric."""
        import string

        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
