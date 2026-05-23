"""Realistic timestamp generation for logs."""

from datetime import datetime, timedelta
import random


class TimeGenerator:
    """Generate realistic timestamps for logs."""

    def __init__(self, start_time: datetime = None, tz_offset: int = 0):
        """
        Initialize time generator.

        Args:
            start_time: Starting time for log generation (default: now)
            tz_offset: Timezone offset in hours
        """
        self.current_time = start_time or datetime.utcnow()
        self.tz_offset = tz_offset
        self.base_time = self.current_time

    def next_timestamp(self, min_seconds: int = 1, max_seconds: int = 60) -> datetime:
        """
        Generate next timestamp with realistic intervals.

        Args:
            min_seconds: Minimum seconds since last event
            max_seconds: Maximum seconds since last event

        Returns:
            Next timestamp
        """
        delta = random.randint(min_seconds, max_seconds)
        self.current_time += timedelta(seconds=delta)
        return self.current_time

    def reset(self):
        """Reset to base time."""
        self.current_time = self.base_time

    def random_timestamp(self, hours_back: int = 24) -> datetime:
        """
        Generate a random timestamp within last N hours.

        Args:
            hours_back: How many hours back to generate

        Returns:
            Random timestamp
        """
        seconds_back = hours_back * 3600
        random_seconds = random.randint(0, seconds_back)
        return datetime.utcnow() - timedelta(seconds=random_seconds)

    def burst_timestamps(self, count: int, min_ms: int = 10, max_ms: int = 100) -> list:
        """
        Generate burst of timestamps (e.g., for attack scenarios).

        Args:
            count: Number of timestamps
            min_ms: Minimum milliseconds between events
            max_ms: Maximum milliseconds between events

        Returns:
            List of timestamps
        """
        timestamps = [self.current_time]
        for _ in range(count - 1):
            ms_delta = random.randint(min_ms, max_ms)
            self.current_time += timedelta(milliseconds=ms_delta)
            timestamps.append(self.current_time)
        return timestamps

    @staticmethod
    def office_hours_timestamp(hours_back: int = 24) -> datetime:
        """
        Generate timestamp during typical office hours (9 AM - 6 PM).

        Args:
            hours_back: How many hours back

        Returns:
            Timestamp during office hours
        """
        base = datetime.utcnow() - timedelta(hours=random.randint(0, hours_back))
        hour = random.randint(9, 17)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return base.replace(hour=hour, minute=minute, second=second)

    @staticmethod
    def off_hours_timestamp(hours_back: int = 24) -> datetime:
        """
        Generate timestamp during off-hours (6 PM - 9 AM).

        Args:
            hours_back: How many hours back

        Returns:
            Timestamp during off-hours
        """
        base = datetime.utcnow() - timedelta(hours=random.randint(0, hours_back))
        hour = random.choice(list(range(0, 9)) + list(range(18, 24)))
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        return base.replace(hour=hour, minute=minute, second=second)
