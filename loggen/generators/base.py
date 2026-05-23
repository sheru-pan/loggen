"""Abstract base generator for log events."""

from abc import ABC, abstractmethod
from typing import Dict, List

from loggen.models.log_event import LogEvent
from loggen.utils.faker_config import FakerProvider
from loggen.utils.timestamps import TimeGenerator


class BaseGenerator(ABC):
    """Abstract base class for log generators."""

    def __init__(self, malicious_ratio: float = 0.2, seed: int = None):
        """
        Initialize generator.

        Args:
            malicious_ratio: Ratio of malicious events (0.0-1.0), default 0.2 (20%)
            seed: Optional seed for reproducibility
        """
        self.malicious_ratio = malicious_ratio
        self.faker = FakerProvider(seed=seed)
        self.time_gen = TimeGenerator()
        self.seed = seed

    @abstractmethod
    def generate(self, count: int = 10, **kwargs) -> List[LogEvent]:
        """
        Generate log events.

        Args:
            count: Number of events to generate
            **kwargs: Generator-specific parameters

        Returns:
            List of LogEvent objects
        """
        pass

    def reset_timestamps(self):
        """Reset timestamp generator."""
        self.time_gen.reset()

    def _should_be_malicious(self) -> bool:
        """Determine if current event should be malicious."""
        return self.faker.is_malicious(self.malicious_ratio)
