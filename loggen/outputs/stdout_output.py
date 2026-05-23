"""Stdout output handler."""

from typing import List

from loggen.models.log_event import LogEvent, LogFormat
from .base import BaseOutputHandler


class StdoutOutputHandler(BaseOutputHandler):
    """Write log events to stdout."""

    def __init__(self, format: LogFormat = LogFormat.RAW):
        """
        Initialize stdout output handler.

        Args:
            format: Output format
        """
        super().__init__(format)

    def write(self, events: List[LogEvent]) -> None:
        """Write events to stdout."""
        for event in events:
            formatted = self._format_event(event)
            print(formatted)
