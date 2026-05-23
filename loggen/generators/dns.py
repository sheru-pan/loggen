"""DNS log generator."""

import random
import string
from typing import List

from loggen.models.log_event import LogEvent, LogLevel
from .base import BaseGenerator


class DNSGenerator(BaseGenerator):
    """Generate DNS query and response logs."""

    SCENARIOS = {
        "query": "Normal DNS queries",
        "dga": "Domain Generation Algorithm (botnet C2)",
        "tunneling": "DNS tunneling for data exfiltration",
        "malicious_domain": "Queries to known malicious domains",
        "zone_transfer": "DNS zone transfer attempts (AXFR)",
        "nxdomain": "High volume of NXDOMAIN responses",
    }

    # Common legitimate domains
    LEGITIMATE_DOMAINS = [
        "google.com",
        "microsoft.com",
        "github.com",
        "stackoverflow.com",
        "wikipedia.org",
        "amazon.com",
        "facebook.com",
        "twitter.com",
        "youtube.com",
        "linkedin.com",
        "reddit.com",
        "office.com",
    ]

    # Known malicious-looking domains (for training only)
    MALICIOUS_DOMAINS = [
        "malware-c2.evil.com",
        "ransomware-payment.bad",
        "phishing-bank.tk",
        "crypto-miner.ml",
        "stealer-c2.ga",
        "trojan-update.cf",
    ]

    # DNS query types
    QUERY_TYPES = ["A", "AAAA", "MX", "TXT", "NS", "PTR", "CNAME", "SOA"]

    def generate(self, count: int = 10, scenario: str = "query", **kwargs) -> List[LogEvent]:
        """Generate DNS logs based on scenario."""
        if scenario == "query":
            return self._generate_query(count)
        elif scenario == "dga":
            return self._generate_dga(count)
        elif scenario == "tunneling":
            return self._generate_tunneling(count)
        elif scenario == "malicious_domain":
            return self._generate_malicious_domain(count)
        elif scenario == "zone_transfer":
            return self._generate_zone_transfer(count)
        elif scenario == "nxdomain":
            return self._generate_nxdomain(count)
        else:
            return self._generate_query(count)

    def _generate_query(self, count: int) -> List[LogEvent]:
        """Generate normal DNS query logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=1, max_seconds=10)

            src_ip = self.faker.ipv4_private()
            domain = random.choice(self.LEGITIMATE_DOMAINS)
            query_type = random.choice(self.QUERY_TYPES)
            response_ip = self.faker.ipv4()

            message = f"DNS query: {src_ip} -> {domain} (type={query_type}) -> {response_ip}"

            event = LogEvent(
                timestamp=timestamp,
                source="dns",
                event_type="dns_query",
                level=LogLevel.INFO,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "query_name": domain,
                    "query_type": query_type,
                    "response_code": "NOERROR",
                    "response_ip": response_ip,
                    "query_size": random.randint(20, 100),
                    "response_size": random.randint(50, 500),
                },
            )
            events.append(event)

        return events

    def _generate_dga(self, count: int) -> List[LogEvent]:
        """Generate Domain Generation Algorithm logs (botnet C2)."""
        events = []

        src_ip = self.faker.ipv4_private()

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=10, max_seconds=60)

            dga_domain = self._generate_dga_domain()
            query_type = "A"
            response_code = random.choice(["NOERROR", "NXDOMAIN", "NXDOMAIN", "NXDOMAIN"])

            message = f"DGA-like query detected: {src_ip} -> {dga_domain} (response={response_code})"

            event = LogEvent(
                timestamp=timestamp,
                source="dns",
                event_type="dga_query",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "query_name": dga_domain,
                    "query_type": query_type,
                    "response_code": response_code,
                    "entropy_score": round(random.uniform(3.5, 4.5), 2),
                    "domain_length": len(dga_domain),
                    "attack_type": "dga",
                },
            )
            events.append(event)

        return events

    def _generate_tunneling(self, count: int) -> List[LogEvent]:
        """Generate DNS tunneling logs (data exfiltration)."""
        events = []

        src_ip = self.faker.ipv4_private()
        c2_domain = "tunnel.attacker.com"

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=1, max_seconds=5)

            encoded_data = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=random.randint(40, 60))
            )
            tunneled_domain = f"{encoded_data}.{c2_domain}"
            query_type = "TXT"

            message = f"Suspicious long DNS query (possible tunneling): {src_ip} -> {tunneled_domain[:80]}..."

            event = LogEvent(
                timestamp=timestamp,
                source="dns",
                event_type="dns_tunneling",
                level=LogLevel.CRITICAL,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "query_name": tunneled_domain,
                    "query_type": query_type,
                    "query_length": len(tunneled_domain),
                    "subdomain_length": len(encoded_data),
                    "attack_type": "dns_tunneling",
                    "exfiltration_bytes": len(encoded_data),
                },
            )
            events.append(event)

        return events

    def _generate_malicious_domain(self, count: int) -> List[LogEvent]:
        """Generate queries to known malicious domains."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=30, max_seconds=300)

            src_ip = self.faker.ipv4_private()
            domain = random.choice(self.MALICIOUS_DOMAINS)
            query_type = random.choice(["A", "AAAA"])

            message = f"Query to known malicious domain: {src_ip} -> {domain}"

            event = LogEvent(
                timestamp=timestamp,
                source="dns",
                event_type="malicious_domain_query",
                level=LogLevel.CRITICAL,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "query_name": domain,
                    "query_type": query_type,
                    "threat_category": random.choice(
                        ["malware", "phishing", "c2", "cryptominer"]
                    ),
                    "threat_intel_source": "internal_blocklist",
                    "action": random.choice(["blocked", "logged"]),
                },
            )
            events.append(event)

        return events

    def _generate_zone_transfer(self, count: int) -> List[LogEvent]:
        """Generate DNS zone transfer attempt logs."""
        events = []

        attacker_ip = self.faker.ipv4()
        target_domains = ["company.internal", "corp.local", "intranet.example.com"]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=2, max_seconds=10)

            domain = random.choice(target_domains)

            message = f"AXFR zone transfer attempt from {attacker_ip} for zone {domain}"

            event = LogEvent(
                timestamp=timestamp,
                source="dns",
                event_type="zone_transfer_attempt",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "src_ip": attacker_ip,
                    "query_name": domain,
                    "query_type": "AXFR",
                    "response_code": "REFUSED",
                    "attack_type": "zone_transfer",
                    "action": "denied",
                },
            )
            events.append(event)

        return events

    def _generate_nxdomain(self, count: int) -> List[LogEvent]:
        """Generate high-volume NXDOMAIN responses (potential malware activity)."""
        events = []

        src_ip = self.faker.ipv4_private()

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=1, max_seconds=3)

            random_domain = f"{self._random_string(8, 15)}.{random.choice(['com', 'net', 'org', 'biz'])}"

            message = f"NXDOMAIN response: {src_ip} -> {random_domain}"

            event = LogEvent(
                timestamp=timestamp,
                source="dns",
                event_type="nxdomain",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "query_name": random_domain,
                    "query_type": "A",
                    "response_code": "NXDOMAIN",
                    "queries_per_minute": random.randint(20, 100),
                },
            )
            events.append(event)

        return events

    @staticmethod
    def _generate_dga_domain() -> str:
        """Generate a DGA-style random domain."""
        length = random.randint(12, 20)
        name = "".join(random.choices(string.ascii_lowercase, k=length))
        tld = random.choice(["com", "net", "info", "biz", "xyz", "top"])
        return f"{name}.{tld}"

    @staticmethod
    def _random_string(min_len: int, max_len: int) -> str:
        """Generate random alphanumeric string."""
        length = random.randint(min_len, max_len)
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
