"""IDS/IPS alert log generator."""

import random
from typing import List

from loggen.models.log_event import LogEvent, LogLevel
from loggen.utils.constants import IDS_MESSAGES
from .base import BaseGenerator


class IDSIPSGenerator(BaseGenerator):
    """Generate IDS/IPS alert logs."""

    SCENARIOS = {
        "alert": "Generic IDS alerts",
        "exploit": "Exploit detection",
        "trojan": "Trojan/malware signatures",
        "anomaly": "Network anomalies",
        "intrusion": "Intrusion attempt detection",
    }

    # Common malware signatures
    MALWARE_FAMILIES = [
        "Emotet",
        "Trickbot",
        "Zerologon",
        "WannaCry",
        "Mirai",
        "Zeus",
        "Conficker",
        "Stuxnet",
    ]

    # CVEs for exploit detection
    CVES = [
        "CVE-2021-44228",  # Log4j
        "CVE-2021-34527",  # PrintNightmare
        "CVE-2021-41773",  # Apache
        "CVE-2020-1938",   # Tomcat
        "CVE-2017-5645",   # ActiveMQ
    ]

    # Signature names
    SIGNATURES = [
        "SQL Injection Attempt",
        "XSS Attack Detected",
        "Buffer Overflow",
        "Command Injection",
        "Remote Code Execution",
        "Privilege Escalation",
        "Suspicious Process Execution",
        "Lateral Movement",
    ]

    def generate(self, count: int = 10, scenario: str = "alert", **kwargs) -> List[LogEvent]:
        """
        Generate IDS/IPS logs.

        Args:
            count: Number of events to generate
            scenario: Scenario type (alert, exploit, trojan, etc.)
            **kwargs: Additional parameters

        Returns:
            List of LogEvent objects
        """
        if scenario == "alert":
            return self._generate_alert(count)
        elif scenario == "exploit":
            return self._generate_exploit(count)
        elif scenario == "trojan":
            return self._generate_trojan(count)
        elif scenario == "anomaly":
            return self._generate_anomaly(count)
        elif scenario == "intrusion":
            return self._generate_intrusion(count)
        else:
            return self._generate_alert(count)

    def _generate_alert(self, count: int) -> List[LogEvent]:
        """Generate generic IDS alerts."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=10, max_seconds=120)

            src_ip = self.faker.ipv4()
            dst_ip = self.faker.ipv4_private()
            signature = random.choice(self.SIGNATURES)

            message = IDS_MESSAGES["alert"].format(
                signature=signature, src_ip=src_ip, dst_ip=dst_ip
            )

            severity = random.choice([LogLevel.WARNING, LogLevel.ERROR])

            event = LogEvent(
                timestamp=timestamp,
                source="ids",
                event_type="ids_alert",
                level=severity,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "signature": signature,
                    "signature_id": random.randint(1000000, 9999999),
                    "priority": random.randint(1, 3),
                    "protocol": random.choice(["tcp", "udp"]),
                    "src_port": self.faker.port(),
                    "dst_port": self.faker.port(well_known=True),
                },
            )
            events.append(event)

        return events

    def _generate_exploit(self, count: int) -> List[LogEvent]:
        """Generate exploit detection logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=5, max_seconds=60)

            src_ip = self.faker.ipv4()
            dst_ip = self.faker.ipv4_private()
            cve = random.choice(self.CVES)

            message = IDS_MESSAGES["exploit"].format(cve=cve, src_ip=src_ip)

            event = LogEvent(
                timestamp=timestamp,
                source="ids",
                event_type="exploit_detected",
                level=LogLevel.CRITICAL,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "cve": cve,
                    "severity": "critical",
                    "confidence": random.randint(80, 100),
                    "payload": "detected",
                },
            )
            events.append(event)

        return events

    def _generate_trojan(self, count: int) -> List[LogEvent]:
        """Generate trojan/malware detection logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=15, max_seconds=300)

            src_ip = self.faker.ipv4()
            dst_ip = self.faker.ipv4_private()
            family = random.choice(self.MALWARE_FAMILIES)

            message = IDS_MESSAGES["trojan"].format(family=family, src_ip=src_ip)

            event = LogEvent(
                timestamp=timestamp,
                source="ids",
                event_type="malware_detected",
                level=LogLevel.CRITICAL,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "malware_family": family,
                    "threat_level": "critical",
                    "file_hash": self._generate_hash(),
                    "detection_method": "signature",
                },
            )
            events.append(event)

        return events

    def _generate_anomaly(self, count: int) -> List[LogEvent]:
        """Generate network anomaly detection logs."""
        events = []

        anomaly_types = [
            "Excessive failed connection attempts",
            "Unusual protocol usage",
            "Abnormal data volume",
            "Suspicious port activity",
            "Unusual timing pattern",
        ]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=30, max_seconds=600)

            src_ip = self.faker.ipv4()
            dst_ip = self.faker.ipv4_private()
            anomaly_type = random.choice(anomaly_types)

            message = IDS_MESSAGES["anomaly"].format(type=anomaly_type, src_ip=src_ip)

            event = LogEvent(
                timestamp=timestamp,
                source="ids",
                event_type="anomaly_detected",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "anomaly_type": anomaly_type,
                    "confidence_score": round(random.uniform(0.6, 0.99), 2),
                    "baseline_value": random.randint(10, 100),
                    "observed_value": random.randint(500, 5000),
                },
            )
            events.append(event)

        return events

    def _generate_intrusion(self, count: int) -> List[LogEvent]:
        """Generate intrusion attempt detection logs."""
        events = []

        attack_types = [
            "Shellcode detection",
            "ROP chain execution",
            "Code injection",
            "Heap spray",
            "Use-after-free",
        ]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=5, max_seconds=30)

            src_ip = self.faker.ipv4()
            dst_ip = self.faker.ipv4_private()
            attack_type = random.choice(attack_types)

            message = f"Intrusion attempt ({attack_type}) from {src_ip} to {dst_ip}"

            event = LogEvent(
                timestamp=timestamp,
                source="ids",
                event_type="intrusion_attempt",
                level=LogLevel.CRITICAL,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "attack_type": attack_type,
                    "block_status": random.choice(["blocked", "detected"]),
                    "target_service": random.choice(["http", "ftp", "smtp", "ssh"]),
                    "payload_size": random.randint(100, 10000),
                },
            )
            events.append(event)

        return events

    @staticmethod
    def _generate_hash() -> str:
        """Generate a random hash."""
        return "".join(random.choices("0123456789abcdef", k=32))
