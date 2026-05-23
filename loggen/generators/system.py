"""System event log generator."""

import random
from typing import List

from loggen.models.log_event import LogEvent, LogLevel
from loggen.utils.constants import SYSTEM_MESSAGES
from .base import BaseGenerator


class SystemGenerator(BaseGenerator):
    """Generate system event logs (Windows, Linux, etc.)."""

    SCENARIOS = {
        "process": "Process creation events",
        "file": "File creation/modification events",
        "registry": "Registry modification (Windows)",
        "service": "Service start/stop events",
        "user": "User account management",
        "privilege": "Privilege escalation attempts",
    }

    # Suspicious processes
    SUSPICIOUS_PROCESSES = [
        "cmd.exe",
        "powershell.exe",
        "rundll32.exe",
        "regsvcs.exe",
        "wmic.exe",
        "psexec.exe",
        "mshta.exe",
        "cscript.exe",
        "bash",
        "sh",
        "perl",
        "python",
    ]

    # Registry keys (Windows)
    REGISTRY_KEYS = [
        "HKLM\\Software\\Microsoft\\Windows\\Run",
        "HKCU\\Software\\Microsoft\\Windows\\Run",
        "HKLM\\Software\\Microsoft\\Windows\\RunOnce",
        "HKCU\\Software\\Microsoft\\Windows\\RunOnce",
        "HKLM\\System\\CurrentControlSet\\Services",
    ]

    # Suspicious file paths
    SUSPICIOUS_FILES = [
        "C:\\Windows\\Temp\\shell.exe",
        "C:\\ProgramData\\system.exe",
        "/tmp/rootkit.sh",
        "/var/tmp/backdoor",
        "~/.ssh/authorized_keys",
        "/etc/passwd",
    ]

    def generate(self, count: int = 10, scenario: str = "process", **kwargs) -> List[LogEvent]:
        """
        Generate system event logs.

        Args:
            count: Number of events to generate
            scenario: Scenario type (process, file, registry, etc.)
            **kwargs: Additional parameters

        Returns:
            List of LogEvent objects
        """
        if scenario == "process":
            return self._generate_process(count)
        elif scenario == "file":
            return self._generate_file(count)
        elif scenario == "registry":
            return self._generate_registry(count)
        elif scenario == "service":
            return self._generate_service(count)
        elif scenario == "user":
            return self._generate_user(count)
        elif scenario == "privilege":
            return self._generate_privilege(count)
        else:
            return self._generate_process(count)

    def _generate_process(self, count: int) -> List[LogEvent]:
        """Generate process creation logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=5, max_seconds=120)

            user = self.faker.username()
            process = random.choice(self.SUSPICIOUS_PROCESSES) if self._should_be_malicious() else self.faker.process_name()
            pid = self.faker.process_id()
            parent_process = random.choice(["explorer.exe", "svchost.exe", "bash", "systemd"])

            message = SYSTEM_MESSAGES["process_creation"].format(
                process=process, pid=pid, user=user
            )

            level = LogLevel.WARNING if process in self.SUSPICIOUS_PROCESSES else LogLevel.INFO

            event = LogEvent(
                timestamp=timestamp,
                source="system",
                event_type="process_creation",
                level=level,
                message=message,
                fields={
                    "user": user,
                    "process": process,
                    "pid": pid,
                    "parent_process": parent_process,
                    "command_line": f"{process} -x hidden" if random.random() < 0.2 else process,
                    "uid": self.faker.user_id() if "unix" in str(parent_process).lower() else None,
                },
            )
            events.append(event)

        return events

    def _generate_file(self, count: int) -> List[LogEvent]:
        """Generate file creation/modification logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=10, max_seconds=300)

            user = self.faker.username()
            file_path = (
                random.choice(self.SUSPICIOUS_FILES)
                if self._should_be_malicious()
                else f"/home/{user}/documents/file_{i}.txt"
            )

            message = SYSTEM_MESSAGES["file_creation"].format(file_path=file_path, user=user)

            level = LogLevel.WARNING if any(s in file_path for s in self.SUSPICIOUS_FILES) else LogLevel.INFO

            event = LogEvent(
                timestamp=timestamp,
                source="system",
                event_type="file_creation",
                level=level,
                message=message,
                fields={
                    "user": user,
                    "file_path": file_path,
                    "file_size": random.randint(0, 10000000),
                    "permissions": "0644",
                    "action": "created",
                },
            )
            events.append(event)

        return events

    def _generate_registry(self, count: int) -> List[LogEvent]:
        """Generate Windows registry modification logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=15, max_seconds=600)

            user = self.faker.username()
            key = random.choice(self.REGISTRY_KEYS)

            message = SYSTEM_MESSAGES["registry_modification"].format(key=key, user=user)

            level = LogLevel.WARNING if "Run" in key else LogLevel.INFO

            event = LogEvent(
                timestamp=timestamp,
                source="system",
                event_type="registry_modification",
                level=level,
                message=message,
                fields={
                    "user": user,
                    "registry_key": key,
                    "value_name": f"Value_{random.randint(1, 100)}",
                    "value_data": self.faker.process_name(),
                    "operation": "Set",
                },
            )
            events.append(event)

        return events

    def _generate_service(self, count: int) -> List[LogEvent]:
        """Generate service start/stop logs."""
        events = []

        services = [
            "sshd",
            "apache2",
            "mysql",
            "postgres",
            "nginx",
            "elasticsearch",
            "redis",
            "kafka",
        ]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=60, max_seconds=3600)

            user = self.faker.username()
            service = random.choice(services)
            action = random.choice(["started", "stopped", "restarted"])

            message = SYSTEM_MESSAGES["service_start"].format(service_name=service, user=user)

            event = LogEvent(
                timestamp=timestamp,
                source="system",
                event_type="service_event",
                level=LogLevel.INFO,
                message=message,
                fields={
                    "user": user,
                    "service": service,
                    "action": action,
                    "status": "success",
                    "exit_code": 0,
                },
            )
            events.append(event)

        return events

    def _generate_user(self, count: int) -> List[LogEvent]:
        """Generate user account management logs."""
        events = []

        actions = ["created", "deleted", "modified", "enabled", "disabled"]

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=300, max_seconds=86400)

            admin_user = self.faker.username()
            new_user = self.faker.username()
            action = random.choice(actions)

            message = SYSTEM_MESSAGES["user_creation"].format(username=new_user)

            level = LogLevel.WARNING if action in ["created", "deleted"] else LogLevel.INFO

            event = LogEvent(
                timestamp=timestamp,
                source="system",
                event_type="user_account",
                level=level,
                message=message,
                fields={
                    "admin_user": admin_user,
                    "target_user": new_user,
                    "action": action,
                    "uid": self.faker.user_id(),
                    "gid": self.faker.group_id(),
                },
            )
            events.append(event)

        return events

    def _generate_privilege(self, count: int) -> List[LogEvent]:
        """Generate privilege escalation logs."""
        events = []

        for i in range(count):
            timestamp = self.time_gen.next_timestamp(min_seconds=30, max_seconds=600)

            user = self.faker.username()
            target_user = random.choice(["root", "system", "administrator"])

            message = SYSTEM_MESSAGES["privilege_escalation"].format(
                user=user, target_user=target_user
            )

            success = not self._should_be_malicious()
            level = LogLevel.INFO if success else LogLevel.ERROR

            event = LogEvent(
                timestamp=timestamp,
                source="system",
                event_type="privilege_escalation",
                level=level,
                message=message,
                fields={
                    "user": user,
                    "target_user": target_user,
                    "method": random.choice(["sudo", "su", "runas", "exploit"]),
                    "result": "success" if success else "failure",
                    "command": "bash" if success else "id",
                },
            )
            events.append(event)

        return events
