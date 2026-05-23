"""File output handler."""

from pathlib import Path
from typing import List

from loggen.models.log_event import LogEvent, LogFormat
from .base import BaseOutputHandler


class FileOutputHandler(BaseOutputHandler):
    """Write log events to a file."""

    def __init__(self, filepath: str, format: LogFormat = LogFormat.RAW, append: bool = False):
        """
        Initialize file output handler.

        Args:
            filepath: Path to output file
            format: Output format
            append: Whether to append or overwrite
        """
        super().__init__(format)
        self.filepath = Path(filepath)
        self.append = append
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def write(self, events: List[LogEvent]) -> None:
        """Write events to file."""
        mode = "a" if (self.append and self.filepath.exists()) else "w"

        with open(self.filepath, mode) as f:
            for event in events:
                formatted = self._format_event(event)
                f.write(formatted + "\n")
