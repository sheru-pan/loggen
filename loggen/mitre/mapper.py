"""MITRE ATT&CK technique mapper - loads techniques and provides lookup."""

import json
from pathlib import Path
from typing import Dict, List, Optional


class MitreMapper:
    """Load and query MITRE ATT&CK techniques from JSON."""

    def __init__(self, techniques_file: Optional[str] = None):
        """
        Initialize the mapper.

        Args:
            techniques_file: Optional path to techniques JSON. Defaults to bundled file.
        """
        if techniques_file is None:
            techniques_file = str(Path(__file__).parent / "techniques.json")

        self.techniques_file = techniques_file
        self.techniques: Dict[str, dict] = {}
        self._load()

    def _load(self) -> None:
        """Load techniques from JSON file."""
        with open(self.techniques_file, "r") as f:
            self.techniques = json.load(f)

    def get_technique(self, technique_id: str) -> Optional[dict]:
        """
        Get technique details by ID.

        Args:
            technique_id: MITRE technique ID (e.g., T1110.001)

        Returns:
            Technique dict or None if not found
        """
        return self.techniques.get(technique_id)

    def list_techniques(self) -> List[str]:
        """List all available technique IDs."""
        return sorted(self.techniques.keys())

    def list_by_tactic(self, tactic: Optional[str] = None) -> Dict[str, List[dict]]:
        """
        Group techniques by tactic.

        Args:
            tactic: Optional tactic name to filter by

        Returns:
            Dict mapping tactic name to list of technique dicts
        """
        grouped: Dict[str, List[dict]] = {}
        for tid, tdata in self.techniques.items():
            tactic_name = tdata.get("tactic", "Unknown")
            if tactic and tactic.lower() != tactic_name.lower():
                continue
            grouped.setdefault(tactic_name, []).append({"id": tid, **tdata})

        for tactic_name in grouped:
            grouped[tactic_name].sort(key=lambda t: t["id"])
        return grouped

    def get_tactics(self) -> List[str]:
        """Get list of all tactics."""
        return sorted({t.get("tactic", "Unknown") for t in self.techniques.values()})

    def search(self, query: str) -> List[dict]:
        """
        Search techniques by name or description.

        Args:
            query: Search string

        Returns:
            List of matching technique dicts (with 'id' included)
        """
        query_lower = query.lower()
        results = []
        for tid, tdata in self.techniques.items():
            name = tdata.get("name", "").lower()
            description = tdata.get("description", "").lower()
            if query_lower in name or query_lower in description or query_lower in tid.lower():
                results.append({"id": tid, **tdata})
        return sorted(results, key=lambda t: t["id"])

    def get_generator_and_scenario(self, technique_id: str) -> Optional[tuple]:
        """
        Get the primary (generator, scenario) tuple for a technique.

        Args:
            technique_id: MITRE technique ID

        Returns:
            Tuple of (generator_name, scenario_name) or None
        """
        technique = self.get_technique(technique_id)
        if not technique:
            return None

        generators = technique.get("generators", [])
        scenarios = technique.get("scenarios", [])

        if not generators or not scenarios:
            return None

        return (generators[0], scenarios[0])

    def get_malicious_ratio(self, technique_id: str) -> float:
        """
        Get the recommended malicious ratio for a technique.

        Args:
            technique_id: MITRE technique ID

        Returns:
            Malicious ratio (0.0-1.0), defaults to 0.5
        """
        technique = self.get_technique(technique_id)
        if not technique:
            return 0.5
        return technique.get("malicious_ratio", 0.5)
