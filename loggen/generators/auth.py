"""Authentication log generator."""

from typing import List
from loggen.models.log_event import LogEvent, LogLevel
from loggen.utils.constants import AUTH_MESSAGES
from .base import BaseGenerator


class AuthGenerator(BaseGenerator):
    """Generate authentication and access logs."""

    SCENARIOS = {
        "bruteforce": "Multiple failed login attempts from same source",
        "successful": "Successful user logins",
        "invalid_user": "Login attempts with non-existent users",
        "privilege_escalation": "sudo/su privilege escalation attempts",
        "account_lockout": "Account lockout due to failed attempts",
        "default_credentials": "Login with default credentials",
    }

    def generate(self, count: int = 10, scenario: str = "bruteforce", **kwargs) -> List[LogEvent]:
        """
        Generate authentication logs.

        Args:
            count: Number of events to generate
            scenario: Scenario type (bruteforce, successful, invalid_user, etc.)
            **kwargs: Additional parameters

        Returns:
            List of LogEvent objects
        """
        if scenario == "bruteforce":
            return self._generate_bruteforce(count)
        elif scenario == "successful":
            return self._generate_successful(count)
        elif scenario == "invalid_user":
            return self._generate_invalid_user(count)
        elif scenario == "privilege_escalation":
            return self._generate_privilege_escalation(count)
        elif scenario == "account_lockout":
            return self._generate_account_lockout(count)
        elif scenario == "default_credentials":
            return self._generate_default_credentials(count)
        else:
            # Default to bruteforce
            return self._generate_bruteforce(count)

    def _generate_bruteforce(self, count: int) -> List[LogEvent]:
        """Generate brute force attack logs."""
        events = []
        src_ip = self.faker.ipv4()
        target_user = self.faker.username()

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=1, max_seconds=5)

            message = AUTH_MESSAGES["failure"].format(
                user=target_user, ip=src_ip, port=self.faker.port()
            )

            event = LogEvent(
                timestamp=timestamp,
                source="auth",
                event_type="ssh_auth_failure",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "user": target_user,
                    "source_ip": src_ip,
                    "port": self.faker.port(),
                    "protocol": "ssh",
                    "attack_type": "brute_force",
                    "attempt": i + 1,
                },
            )
            events.append(event)

        return events

    def _generate_successful(self, count: int) -> List[LogEvent]:
        """Generate successful login logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=10, max_seconds=600)

            user = self.faker.username()
            src_ip = self.faker.ipv4()

            message = AUTH_MESSAGES["success"].format(user=user, ip=src_ip)

            event = LogEvent(
                timestamp=timestamp,
                source="auth",
                event_type="ssh_auth_success",
                level=LogLevel.INFO,
                message=message,
                fields={
                    "user": user,
                    "source_ip": src_ip,
                    "port": self.faker.port(),
                    "protocol": "ssh",
                    "auth_method": "password",
                },
            )
            events.append(event)

        return events

    def _generate_invalid_user(self, count: int) -> List[LogEvent]:
        """Generate invalid user login attempts."""
        events = []
        src_ip = self.faker.ipv4()

        invalid_users = ["admin", "root", "test", "guest", "oracle", "postgres"]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=2, max_seconds=10)

            user = invalid_users[i % len(invalid_users)]
            message = AUTH_MESSAGES["invalid_user"].format(
                user=user, ip=src_ip, port=self.faker.port()
            )

            event = LogEvent(
                timestamp=timestamp,
                source="auth",
                event_type="ssh_invalid_user",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "user": user,
                    "source_ip": src_ip,
                    "port": self.faker.port(),
                    "protocol": "ssh",
                    "result": "invalid_user",
                },
            )
            events.append(event)

        return events

    def _generate_privilege_escalation(self, count: int) -> List[LogEvent]:
        """Generate privilege escalation logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=30, max_seconds=300)

            user = self.faker.username()
            message = AUTH_MESSAGES["sudo"].format(user=user)

            level = LogLevel.WARNING if self._should_be_malicious() else LogLevel.INFO

            event = LogEvent(
                timestamp=timestamp,
                source="auth",
                event_type="sudo_execution",
                level=level,
                message=message,
                fields={
                    "user": user,
                    "target_user": "root",
                    "command": "/bin/bash",
                    "result": "success",
                    "tty": "pts/0",
                },
            )
            events.append(event)

        return events

    def _generate_account_lockout(self, count: int) -> List[LogEvent]:
        """Generate account lockout logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=60, max_seconds=600)

            user = self.faker.username()
            failed_attempts = self.faker.random_int(min=5, max=10)
            message = AUTH_MESSAGES["lockout"].format(user=user, count=failed_attempts)

            event = LogEvent(
                timestamp=timestamp,
                source="auth",
                event_type="account_lockout",
                level=LogLevel.ERROR,
                message=message,
                fields={
                    "user": user,
                    "failed_attempts": failed_attempts,
                    "lockout_duration": "15 minutes",
                },
            )
            events.append(event)

        return events

    def _generate_default_credentials(self, count: int) -> List[LogEvent]:
        """Generate default credential login logs."""
        events = []

        default_users = ["admin", "root", "test", "guest"]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=5, max_seconds=60)

            user = default_users[i % len(default_users)]
            src_ip = self.faker.ipv4()

            message = AUTH_MESSAGES["success"].format(user=user, ip=src_ip)

            event = LogEvent(
                timestamp=timestamp,
                source="auth",
                event_type="ssh_auth_success",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "user": user,
                    "source_ip": src_ip,
                    "port": self.faker.port(),
                    "protocol": "ssh",
                    "auth_method": "password",
                    "credential_type": "default",
                    "risk": "high",
                },
            )
            events.append(event)

        return events
