"""Scenario configuration model."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Scenario(BaseModel):
    """Configuration for a log generation scenario."""

    name: str = Field(description="Scenario name")
    generator_type: str = Field(description="Generator to use (auth, firewall, etc.)")
    description: str = Field(description="Human-readable description")
    count: int = Field(default=10, description="Number of logs to generate")
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Generator-specific parameters"
    )
    mitre_techniques: Optional[List[str]] = Field(
        default=None, description="Associated MITRE ATT&CK techniques (e.g., T1110.001)"
    )
    keywords: Optional[List[str]] = Field(default=None, description="Search keywords")

    class Config:
        """Pydantic config."""

        extra = "allow"
