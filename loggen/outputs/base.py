"""Abstract base output handler."""

from abc import ABC, abstractmethod
from typing import List

from loggen.models.log_event import LogEvent, LogFormat


class BaseOutputHandler(ABC):
    """Abstract base class for output handlers."""

    def __init__(self, format: LogFormat = LogFormat.RAW):
        """
        Initialize output handler.

        Args:
            format: Output format (raw, json, cef, syslog)
        """
        self.format = format

    @abstractmethod
    def write(self, events: List[LogEvent]) -> None:
        """
        Write events to output destination.

        Args:
            events: List of LogEvent objects to write
        """
        pass

    def _format_event(self, event: LogEvent) -> str:
        """Format event based on configured format."""
        if self.format == LogFormat.JSON:
            return event.to_json()
        elif self.format == LogFormat.CEF:
            return event.to_cef()
        elif self.format == LogFormat.SYSLOG:
            return event.to_syslog()
        else:
            return event.to_raw()
