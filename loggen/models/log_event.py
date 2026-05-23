"""Base log event model."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel, Field


class LogFormat(str, Enum):
    """Supported log output formats."""

    RAW = "raw"
    JSON = "json"
    CEF = "cef"
    SYSLOG = "syslog"


class LogLevel(str, Enum):
    """Log severity levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEvent(BaseModel):
    """Base log event model."""

    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Event timestamp")
    source: str = Field(description="Log source (e.g., auth, firewall)")
    event_type: str = Field(description="Type of event")
    level: LogLevel = Field(default=LogLevel.INFO, description="Severity level")
    message: str = Field(description="Log message")
    fields: Dict[str, Any] = Field(default_factory=dict, description="Additional fields")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump()

    def to_json(self) -> str:
        """Convert to JSON string."""
        return self.model_dump_json()

    def to_raw(self) -> str:
        """Convert to raw log format."""
        timestamp_str = self.timestamp.isoformat()
        return f"{timestamp_str} {self.source} [{self.level.value}] {self.event_type}: {self.message}"

    def to_cef(self) -> str:
        """Convert to CEF (Common Event Format)."""
        cef_version = "0"
        device_vendor = "loggen"
        device_product = self.source
        device_version = "1.0"
        signature_id = self.event_type
        name = self.message
        severity = self._severity_to_cef_number()

        extensions = " ".join(
            [f"{k}={v}" for k, v in self.fields.items() if v is not None]
        )

        cef_str = f"CEF:{cef_version}|{device_vendor}|{device_product}|{device_version}|{signature_id}|{name}|{severity}"
        if extensions:
            cef_str += f"|{extensions}"

        return cef_str

    def _severity_to_cef_number(self) -> int:
        """Convert LogLevel to CEF severity number (0-10)."""
        mapping = {
            LogLevel.DEBUG: 1,
            LogLevel.INFO: 2,
            LogLevel.WARNING: 5,
            LogLevel.ERROR: 8,
            LogLevel.CRITICAL: 10,
        }
        return mapping.get(self.level, 2)

    def to_syslog(self) -> str:
        """Convert to syslog format."""
        facility = 16  # local0
        severity = {
            LogLevel.DEBUG: 7,
            LogLevel.INFO: 6,
            LogLevel.WARNING: 4,
            LogLevel.ERROR: 3,
            LogLevel.CRITICAL: 2,
        }.get(self.level, 6)
        priority = facility * 8 + severity

        timestamp_str = self.timestamp.strftime("%b %d %H:%M:%S")
        hostname = "loggen-host"

        return f"<{priority}>{timestamp_str} {hostname} {self.source}[{self.event_type}]: {self.message}"
