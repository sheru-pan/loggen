"""Loggen CLI - Main entry point."""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from loggen.generators.auth import AuthGenerator
from loggen.generators.firewall import FirewallGenerator
from loggen.generators.ids_ips import IDSIPSGenerator
from loggen.generators.web import WebGenerator
from loggen.generators.system import SystemGenerator
from loggen.generators.dns import DNSGenerator
from loggen.generators.email import EmailGenerator
from loggen.generators.cloud import CloudGenerator
from loggen.mitre.mapper import MitreMapper
from loggen.models.log_event import LogFormat
from loggen.outputs.file_output import FileOutputHandler
from loggen.outputs.stdout_output import StdoutOutputHandler

app = typer.Typer(help="Generate realistic SOC analyst training logs")
console = Console()


# Generator registry - maps name to (class, default_malicious_ratio)
GENERATOR_REGISTRY = {
    "auth": (AuthGenerator, 0.3),
    "firewall": (FirewallGenerator, 0.25),
    "ids": (IDSIPSGenerator, 0.8),
    "web": (WebGenerator, 0.35),
    "system": (SystemGenerator, 0.25),
    "dns": (DNSGenerator, 0.3),
    "email": (EmailGenerator, 0.4),
    "cloud": (CloudGenerator, 0.3),
}


def _run_generator(
    generator_name: str,
    scenario: str,
    count: int,
    output: Optional[str],
    format: str,
    malicious_ratio: Optional[float] = None,
) -> None:
    """Shared logic for running a generator and writing output."""
    try:
        log_format = LogFormat(format)
    except ValueError:
        console.print(f"[red]Invalid format: {format}. Valid: raw, json, cef, syslog[/red]")
        raise typer.Exit(1)

    if generator_name not in GENERATOR_REGISTRY:
        console.print(f"[red]Unknown generator: {generator_name}[/red]")
        raise typer.Exit(1)

    generator_class, default_ratio = GENERATOR_REGISTRY[generator_name]
    ratio = malicious_ratio if malicious_ratio is not None else default_ratio
    generator = generator_class(malicious_ratio=ratio)
    events = generator.generate(count=count, scenario=scenario)

    if output:
        handler = FileOutputHandler(output, format=log_format)
        handler.write(events)
        console.print(f"[green]✓ Generated {count} logs to {output}[/green]")
    else:
        handler = StdoutOutputHandler(format=log_format)
        handler.write(events)


@app.command()
def auth(
    scenario: str = typer.Argument("bruteforce", help="bruteforce, successful, invalid_user, privilege_escalation, account_lockout, default_credentials"),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate authentication logs."""
    _run_generator("auth", scenario, count, output, format)


@app.command()
def firewall(
    scenario: str = typer.Argument("blocked", help="blocked, portscan, ddos, allowed, unusual_traffic"),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate firewall logs."""
    _run_generator("firewall", scenario, count, output, format)


@app.command()
def ids(
    scenario: str = typer.Argument("alert", help="alert, exploit, trojan, anomaly, intrusion"),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate IDS/IPS logs."""
    _run_generator("ids", scenario, count, output, format)


@app.command()
def web(
    scenario: str = typer.Argument("attack", help="attack, normal, scan, unauthorized, abuse"),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate web server logs."""
    _run_generator("web", scenario, count, output, format)


@app.command()
def system(
    scenario: str = typer.Argument("process", help="process, file, registry, service, user, privilege"),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate system event logs."""
    _run_generator("system", scenario, count, output, format)


@app.command()
def dns(
    scenario: str = typer.Argument("query", help="query, dga, tunneling, malicious_domain, zone_transfer, nxdomain"),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate DNS logs (queries, DGA, tunneling, malicious domains)."""
    _run_generator("dns", scenario, count, output, format)


@app.command()
def email(
    scenario: str = typer.Argument("phishing", help="phishing, malware_attachment, bec, spoofing, spam, normal"),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate email server logs (phishing, BEC, malware attachments)."""
    _run_generator("email", scenario, count, output, format)


@app.command()
def cloud(
    scenario: str = typer.Argument("console_login", help="console_login, iam_changes, bucket_access, key_creation, suspicious_api, resource_changes"),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate cloud audit logs (AWS CloudTrail style)."""
    _run_generator("cloud", scenario, count, output, format)


@app.command()
def mitre(
    technique_id: str = typer.Argument(..., help="MITRE ATT&CK technique ID (e.g., T1110.001)"),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate logs for a specific MITRE ATT&CK technique."""
    mapper = MitreMapper()
    technique = mapper.get_technique(technique_id)

    if technique is None:
        console.print(f"[red]Technique {technique_id} not found.[/red]")
        console.print("[yellow]Run 'loggen list --type mitre' to see available techniques.[/yellow]")
        raise typer.Exit(1)

    result = mapper.get_generator_and_scenario(technique_id)
    if result is None:
        console.print(f"[red]No generator mapping for {technique_id}[/red]")
        raise typer.Exit(1)

    generator_name, scenario = result
    malicious_ratio = mapper.get_malicious_ratio(technique_id)

    console.print(f"[bold cyan]MITRE ATT&CK Technique: {technique_id}[/bold cyan]")
    console.print(f"[cyan]Name:[/cyan] {technique['name']}")
    console.print(f"[cyan]Tactic:[/cyan] {technique['tactic']}")
    console.print(f"[cyan]Generator:[/cyan] {generator_name} (scenario: {scenario}, malicious_ratio: {malicious_ratio})")
    console.print("")

    _run_generator(generator_name, scenario, count, output, format, malicious_ratio=malicious_ratio)


@app.command(name="list")
def list_command(
    type: str = typer.Option("scenarios", "--type", "-t", help="List type: scenarios, generators, mitre, tactics"),
    tactic: Optional[str] = typer.Option(None, "--tactic", help="Filter MITRE techniques by tactic"),
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Search MITRE techniques by keyword"),
) -> None:
    """List available scenarios, generators, MITRE techniques, or tactics."""
    if type == "scenarios":
        _list_scenarios()
    elif type == "generators":
        _list_generators()
    elif type == "mitre":
        _list_mitre(tactic=tactic, search=search)
    elif type == "tactics":
        _list_tactics()
    else:
        console.print(f"[red]Unknown type: {type}. Valid: scenarios, generators, mitre, tactics[/red]")
        raise typer.Exit(1)


def _list_scenarios() -> None:
    """List all available scenarios across generators."""
    table = Table(title="Available Scenarios")
    table.add_column("Generator", style="cyan", no_wrap=True)
    table.add_column("Scenario", style="magenta")
    table.add_column("Description", style="green")

    for gen_name, (gen_class, _) in GENERATOR_REGISTRY.items():
        scenarios = getattr(gen_class, "SCENARIOS", {})
        for scenario_name, description in scenarios.items():
            table.add_row(gen_name, scenario_name, description)

    console.print(table)


def _list_generators() -> None:
    """List all available generators."""
    table = Table(title="Available Generators")
    table.add_column("Generator", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Default Malicious Ratio", style="yellow")

    descriptions = {
        "auth": "Authentication and access logs (SSH, login events)",
        "firewall": "Firewall and network logs (blocks, scans, DDoS)",
        "ids": "IDS/IPS alerts (exploits, malware, anomalies)",
        "web": "Web server logs (HTTP, SQLi, XSS, RCE)",
        "system": "System events (process, file, registry, services)",
        "dns": "DNS logs (queries, DGA, tunneling, malicious domains)",
        "email": "Email server logs (phishing, BEC, malware attachments)",
        "cloud": "Cloud audit logs (AWS CloudTrail: IAM, S3, console)",
    }

    for gen_name, (_, ratio) in GENERATOR_REGISTRY.items():
        table.add_row(gen_name, descriptions.get(gen_name, ""), f"{ratio:.0%}")

    console.print(table)


def _list_mitre(tactic: Optional[str] = None, search: Optional[str] = None) -> None:
    """List MITRE ATT&CK techniques."""
    mapper = MitreMapper()

    if search:
        results = mapper.search(search)
        title = f"MITRE Techniques matching '{search}'"
    else:
        grouped = mapper.list_by_tactic(tactic=tactic)
        results = []
        for tactic_name in sorted(grouped.keys()):
            results.extend(grouped[tactic_name])
        title = f"MITRE Techniques" + (f" - {tactic}" if tactic else "")

    if not results:
        console.print(f"[yellow]No techniques found.[/yellow]")
        return

    table = Table(title=title)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Tactic", style="blue")
    table.add_column("Generator", style="green")

    for technique in results:
        generators = ", ".join(technique.get("generators", []))
        table.add_row(
            technique["id"],
            technique.get("name", ""),
            technique.get("tactic", ""),
            generators,
        )

    console.print(table)
    console.print(f"\n[bold]Total: {len(results)} techniques[/bold]")


def _list_tactics() -> None:
    """List MITRE ATT&CK tactics."""
    mapper = MitreMapper()
    tactics = mapper.get_tactics()
    grouped = mapper.list_by_tactic()

    table = Table(title="MITRE ATT&CK Tactics")
    table.add_column("Tactic", style="cyan")
    table.add_column("Technique Count", style="yellow")

    for tactic in tactics:
        count = len(grouped.get(tactic, []))
        table.add_row(tactic, str(count))

    console.print(table)


if __name__ == "__main__":
    app()
