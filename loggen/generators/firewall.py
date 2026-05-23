"""Firewall log generator."""

import random
from typing import List

from loggen.models.log_event import LogEvent, LogLevel
from loggen.utils.constants import FIREWALL_MESSAGES
from .base import BaseGenerator


class FirewallGenerator(BaseGenerator):
    """Generate firewall and network logs."""

    SCENARIOS = {
        "blocked": "Blocked connection attempts",
        "portscan": "Port scanning activity",
        "ddos": "DDoS attack traffic",
        "allowed": "Allowed connections",
        "unusual_traffic": "Unusual traffic patterns",
    }

    def generate(self, count: int = 10, scenario: str = "blocked", **kwargs) -> List[LogEvent]:
        """
        Generate firewall logs.

        Args:
            count: Number of events to generate
            scenario: Scenario type (blocked, portscan, ddos, etc.)
            **kwargs: Additional parameters

        Returns:
            List of LogEvent objects
        """
        if scenario == "blocked":
            return self._generate_blocked(count)
        elif scenario == "portscan":
            return self._generate_portscan(count)
        elif scenario == "ddos":
            return self._generate_ddos(count)
        elif scenario == "allowed":
            return self._generate_allowed(count)
        elif scenario == "unusual_traffic":
            return self._generate_unusual_traffic(count)
        else:
            return self._generate_blocked(count)

    def _generate_blocked(self, count: int) -> List[LogEvent]:
        """Generate blocked connection logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=5, max_seconds=30)

            src_ip = self.faker.ipv4()
            dst_ip = self.faker.ipv4_private()
            src_port = self.faker.port()
            dst_port = self.faker.port(well_known=True)
            protocol = random.choice(["TCP", "UDP"])

            message = FIREWALL_MESSAGES["blocked"].format(
                protocol=protocol,
                src_ip=src_ip,
                src_port=src_port,
                dst_ip=dst_ip,
                dst_port=dst_port,
            )

            event = LogEvent(
                timestamp=timestamp,
                source="firewall",
                event_type="blocked_connection",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "src_port": src_port,
                    "dst_port": dst_port,
                    "protocol": protocol,
                    "action": "block",
                    "rule_id": f"FW-{random.randint(1000, 9999)}",
                },
            )
            events.append(event)

        return events

    def _generate_portscan(self, count: int) -> List[LogEvent]:
        """Generate port scan detection logs."""
        events = []

        attacker_ip = self.faker.ipv4()
        target_ip = self.faker.ipv4_private()
        ports_scanned = [22, 80, 443, 3389, 3306, 5432, 8080]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=1, max_seconds=3)

            port_range = f"{ports_scanned[0]}-{ports_scanned[-1]}"
            message = FIREWALL_MESSAGES["port_scan"].format(
                src_ip=attacker_ip, port_range=port_range
            )

            event = LogEvent(
                timestamp=timestamp,
                source="firewall",
                event_type="port_scan",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "src_ip": attacker_ip,
                    "dst_ip": target_ip,
                    "ports_scanned": ports_scanned,
                    "scan_type": "syn_scan",
                    "packets_sent": random.randint(100, 1000),
                },
            )
            events.append(event)

        return events

    def _generate_ddos(self, count: int) -> List[LogEvent]:
        """Generate DDoS attack logs."""
        events = []

        attacker_ips = [self.faker.ipv4() for _ in range(5)]
        target_ip = self.faker.ipv4_private()

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=1, max_seconds=2)

            src_ip = random.choice(attacker_ips)
            packet_count = random.randint(1000, 10000)
            seconds = random.randint(1, 5)

            message = FIREWALL_MESSAGES["ddos"].format(
                src_ip=src_ip, packet_count=packet_count, seconds=seconds
            )

            event = LogEvent(
                timestamp=timestamp,
                source="firewall",
                event_type="ddos_attack",
                level=LogLevel.CRITICAL,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "dst_ip": target_ip,
                    "packet_count": packet_count,
                    "duration_seconds": seconds,
                    "attack_type": "udp_flood",
                    "packets_per_second": packet_count // seconds,
                },
            )
            events.append(event)

        return events

    def _generate_allowed(self, count: int) -> List[LogEvent]:
        """Generate allowed connection logs (baseline traffic)."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=10, max_seconds=120)

            src_ip = self.faker.ipv4_private()
            dst_ip = self.faker.ipv4()
            src_port = self.faker.port()
            dst_port = self.faker.port(well_known=True)
            protocol = random.choice(["TCP", "UDP"])

            message = FIREWALL_MESSAGES["allowed"].format(
                protocol=protocol,
                src_ip=src_ip,
                src_port=src_port,
                dst_ip=dst_ip,
                dst_port=dst_port,
            )

            event = LogEvent(
                timestamp=timestamp,
                source="firewall",
                event_type="allowed_connection",
                level=LogLevel.INFO,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "src_port": src_port,
                    "dst_port": dst_port,
                    "protocol": protocol,
                    "action": "allow",
                    "rule_id": f"FW-{random.randint(100, 999)}",
                    "bytes_transferred": random.randint(1024, 1024000),
                },
            )
            events.append(event)

        return events

    def _generate_unusual_traffic(self, count: int) -> List[LogEvent]:
        """Generate unusual traffic pattern logs."""
        events = []

        patterns = [
            "Large data transfer to external IP",
            "Connection to unusual port",
            "Bidirectional traffic on non-standard port",
            "Multiple protocol violations",
        ]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=30, max_seconds=300)

            src_ip = self.faker.ipv4_private()
            dst_ip = self.faker.ipv4()
            pattern = random.choice(patterns)

            message = f"Unusual traffic: {pattern} from {src_ip} to {dst_ip}"

            event = LogEvent(
                timestamp=timestamp,
                source="firewall",
                event_type="unusual_traffic",
                level=LogLevel.WARNING,
                message=message,
                fields={
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "pattern": pattern,
                    "bytes": random.randint(1000000, 100000000),
                    "duration": random.randint(60, 3600),
                },
            )
            events.append(event)

        return events
