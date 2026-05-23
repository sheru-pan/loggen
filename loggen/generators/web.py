"""Web server log generator."""

import random
from typing import List

from loggen.models.log_event import LogEvent, LogLevel
from loggen.utils.constants import WEB_MESSAGES, HTTP_ATTACK_PATHS
from .base import BaseGenerator


class WebGenerator(BaseGenerator):
    """Generate web server logs."""

    SCENARIOS = {
        "attack": "Web-based attacks (SQLi, XSS, etc.)",
        "normal": "Normal web traffic",
        "scan": "Web vulnerability scanning",
        "unauthorized": "Unauthorized access attempts",
        "abuse": "Resource abuse (rate limiting, etc.)",
    }

    # Common attack payloads
    ATTACK_PARAMS = {
        "sql_injection": ["' OR '1'='1", "'; DROP TABLE--", "UNION SELECT"],
        "xss": ["<script>", "onerror=", "onload="],
        "command_injection": ["; cat /etc/passwd", "| whoami", "` id `"],
        "path_traversal": ["../", "..\\", "%2e%2e"],
    }

    def generate(self, count: int = 10, scenario: str = "attack", **kwargs) -> List[LogEvent]:
        """
        Generate web server logs.

        Args:
            count: Number of events to generate
            scenario: Scenario type (attack, normal, scan, etc.)
            **kwargs: Additional parameters

        Returns:
            List of LogEvent objects
        """
        if scenario == "attack":
            return self._generate_attack(count)
        elif scenario == "normal":
            return self._generate_normal(count)
        elif scenario == "scan":
            return self._generate_scan(count)
        elif scenario == "unauthorized":
            return self._generate_unauthorized(count)
        elif scenario == "abuse":
            return self._generate_abuse(count)
        else:
            return self._generate_attack(count)

    def _generate_attack(self, count: int) -> List[LogEvent]:
        """Generate web attack logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=2, max_seconds=15)

            src_ip = self.faker.ipv4()
            method = self.faker.http_method()
            path = random.choice(HTTP_ATTACK_PATHS)
            status = 400  # Bad request / blocked
            user_agent = self.faker.user_agent()

            if random.random() < 0.3:  # 30% SQL injection
                payload = self.faker.sql_injection_payload()
                message = WEB_MESSAGES["sql_injection"].format(param="id")
                event_type = "sql_injection"
            elif random.random() < 0.5:  # 20% XSS
                payload = self.faker.xss_payload()
                message = WEB_MESSAGES["xss"].format(location="parameter")
                event_type = "xss_attempt"
            elif random.random() < 0.7:  # 20% Path traversal
                payload = self.faker.path_traversal_payload()
                message = WEB_MESSAGES["path_traversal"].format(path=path)
                event_type = "path_traversal"
            else:  # 30% Command injection
                payload = self.faker.command_injection_payload()
                message = WEB_MESSAGES["command_injection"]
                event_type = "command_injection"

            event = LogEvent(
                timestamp=timestamp,
                source="web",
                event_type=event_type,
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "method": method,
                    "path": path,
                    "status_code": status,
                    "user_agent": user_agent,
                    "payload": payload[:50],  # Truncate for readability
                    "referer": self.faker.referer(),
                    "response_size": random.randint(0, 500),
                },
            )
            events.append(event)

        return events

    def _generate_normal(self, count: int) -> List[LogEvent]:
        """Generate normal web traffic logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=1, max_seconds=30)

            src_ip = self.faker.ipv4()
            method = self.faker.http_method()
            path = "/" if random.random() < 0.3 else f"/api/v1/{random.choice(['users', 'posts', 'data'])}"
            status = self.faker.http_status_code(success=True)
            user_agent = self.faker.user_agent()
            response_size = random.randint(1000, 1000000)

            message = WEB_MESSAGES["request"].format(
                method=method,
                path=path,
                status=status,
                bytes=response_size,
                user_agent=user_agent[:50],
            )

            event = LogEvent(
                timestamp=timestamp,
                source="web",
                event_type="http_request",
                level=LogLevel.INFO,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "method": method,
                    "path": path,
                    "status_code": status,
                    "user_agent": user_agent,
                    "response_size": response_size,
                    "response_time_ms": random.randint(10, 500),
                    "referer": self.faker.referer() if random.random() < 0.7 else "-",
                },
            )
            events.append(event)

        return events

    def _generate_scan(self, count: int) -> List[LogEvent]:
        """Generate web vulnerability scan logs."""
        events = []

        scanner_ips = [self.faker.ipv4() for _ in range(3)]
        scan_paths = [
            "/admin",
            "/login",
            "/wp-admin",
            "/config",
            ".git",
            ".env",
            "web.config",
        ]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=2, max_seconds=10)

            src_ip = random.choice(scanner_ips)
            path = random.choice(scan_paths)
            method = "GET"
            status = random.choice([404, 403, 401])

            message = f"Vulnerability scan attempt: {method} {path} {status} from {src_ip}"

            event = LogEvent(
                timestamp=timestamp,
                source="web",
                event_type="vuln_scan",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "method": method,
                    "path": path,
                    "status_code": status,
                    "user_agent": "Scanner/1.0",
                    "scan_type": "web_crawl",
                },
            )
            events.append(event)

        return events

    def _generate_unauthorized(self, count: int) -> List[LogEvent]:
        """Generate unauthorized access attempt logs."""
        events = []

        resources = ["/admin", "/internal", "/api/sensitive", "/backup", "/config.php"]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=5, max_seconds=60)

            src_ip = self.faker.ipv4()
            user = self.faker.username()
            resource = random.choice(resources)

            message = WEB_MESSAGES["unauthorized"].format(resource=resource, user=user)

            event = LogEvent(
                timestamp=timestamp,
                source="web",
                event_type="unauthorized_access",
                level=LogLevel.ERROR,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "user": user,
                    "resource": resource,
                    "status_code": 403,
                    "attempt": i + 1,
                },
            )
            events.append(event)

        return events

    def _generate_abuse(self, count: int) -> List[LogEvent]:
        """Generate resource abuse/rate limit logs."""
        events = []

        src_ip = self.faker.ipv4()
        paths = ["/api/users", "/search", "/download", "/upload"]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=1, max_seconds=5)

            path = random.choice(paths)
            request_count = random.randint(100, 1000)

            message = f"Rate limit exceeded: {request_count} requests from {src_ip} to {path}"

            event = LogEvent(
                timestamp=timestamp,
                source="web",
                event_type="rate_limit",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "path": path,
                    "request_count": request_count,
                    "threshold": 100,
                    "action": "blocked",
                    "duration": "5 minutes",
                },
            )
            events.append(event)

        return events
