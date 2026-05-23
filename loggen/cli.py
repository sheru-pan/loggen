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
from loggen.models.log_event import LogFormat
from loggen.outputs.file_output import FileOutputHandler
from loggen.outputs.stdout_output import StdoutOutputHandler

app = typer.Typer(help="Generate realistic SOC analyst training logs")
console = Console()


@app.command()
def auth(
    scenario: str = typer.Argument("bruteforce", help="Scenario: bruteforce, successful, etc."),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate authentication logs."""
    try:
        log_format = LogFormat(format)
    except ValueError:
        console.print(f"[red]Invalid format: {format}[/red]")
        raise typer.Exit(1)

    generator = AuthGenerator(malicious_ratio=0.3)
    events = generator.generate(count=count, scenario=scenario)

    if output:
        handler = FileOutputHandler(output, format=log_format)
        handler.write(events)
        console.print(f"[green]✓ Generated {count} logs to {output}[/green]")
    else:
        handler = StdoutOutputHandler(format=log_format)
        handler.write(events)


@app.command()
def firewall(
    scenario: str = typer.Argument("blocked", help="Scenario: blocked, portscan, etc."),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate firewall logs."""
    try:
        log_format = LogFormat(format)
    except ValueError:
        console.print(f"[red]Invalid format: {format}[/red]")
        raise typer.Exit(1)

    generator = FirewallGenerator(malicious_ratio=0.25)
    events = generator.generate(count=count, scenario=scenario)

    if output:
        handler = FileOutputHandler(output, format=log_format)
        handler.write(events)
        console.print(f"[green]✓ Generated {count} logs to {output}[/green]")
    else:
        handler = StdoutOutputHandler(format=log_format)
        handler.write(events)


@app.command()
def ids(
    scenario: str = typer.Argument("alert", help="Scenario: alert, exploit, etc."),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate IDS/IPS logs."""
    try:
        log_format = LogFormat(format)
    except ValueError:
        console.print(f"[red]Invalid format: {format}[/red]")
        raise typer.Exit(1)

    generator = IDSIPSGenerator(malicious_ratio=0.8)
    events = generator.generate(count=count, scenario=scenario)

    if output:
        handler = FileOutputHandler(output, format=log_format)
        handler.write(events)
        console.print(f"[green]✓ Generated {count} logs to {output}[/green]")
    else:
        handler = StdoutOutputHandler(format=log_format)
        handler.write(events)


@app.command()
def web(
    scenario: str = typer.Argument("attack", help="Scenario: attack, normal, etc."),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate web server logs."""
    try:
        log_format = LogFormat(format)
    except ValueError:
        console.print(f"[red]Invalid format: {format}[/red]")
        raise typer.Exit(1)

    generator = WebGenerator(malicious_ratio=0.35)
    events = generator.generate(count=count, scenario=scenario)

    if output:
        handler = FileOutputHandler(output, format=log_format)
        handler.write(events)
        console.print(f"[green]✓ Generated {count} logs to {output}[/green]")
    else:
        handler = StdoutOutputHandler(format=log_format)
        handler.write(events)


@app.command()
def system(
    scenario: str = typer.Argument("process", help="Scenario: process, registry, etc."),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate system event logs."""
    try:
        log_format = LogFormat(format)
    except ValueError:
        console.print(f"[red]Invalid format: {format}[/red]")
        raise typer.Exit(1)

    generator = SystemGenerator(malicious_ratio=0.25)
    events = generator.generate(count=count, scenario=scenario)

    if output:
        handler = FileOutputHandler(output, format=log_format)
        handler.write(events)
        console.print(f"[green]✓ Generated {count} logs to {output}[/green]")
    else:
        handler = StdoutOutputHandler(format=log_format)
        handler.write(events)


@app.command()
def mitre(
    technique_id: str = typer.Argument(..., help="MITRE ATT&CK technique ID (e.g., T1110.001)"),
    count: int = typer.Option(10, "--count", "-c", help="Number of logs to generate"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    format: str = typer.Option("raw", "--format", "-f", help="Output format: raw, json, cef, syslog"),
) -> None:
    """Generate logs for a specific MITRE ATT&CK technique."""
    try:
        log_format = LogFormat(format)
    except ValueError:
        console.print(f"[red]Invalid format: {format}[/red]")
        raise typer.Exit(1)

    # For now, map technique IDs to generators
    # T1110.001 = Brute Force: Password Guessing
    technique_mapping = {
        "T1110.001": ("auth", "bruteforce"),
        "T1110.003": ("web", "attack"),
        "T1078.001": ("auth", "default_credentials"),
        "T1021.006": ("auth", "privilege_escalation"),
        "T1021.001": ("firewall", "allowed"),
        "T1040.001": ("firewall", "portscan"),
        "T1056": ("ids", "alert"),
    }

    if technique_id not in technique_mapping:
        console.print(f"[yellow]Technique {technique_id} not found. Using auth brute force.[/yellow]")
        generator_type, scenario = "auth", "bruteforce"
    else:
        generator_type, scenario = technique_mapping[technique_id]

    if generator_type == "auth":
        generator = AuthGenerator(malicious_ratio=0.7)
    elif generator_type == "firewall":
        generator = FirewallGenerator(malicious_ratio=0.6)
    elif generator_type == "ids":
        generator = IDSIPSGenerator(malicious_ratio=0.8)
    elif generator_type == "web":
        generator = WebGenerator(malicious_ratio=0.6)
    else:
        generator = AuthGenerator(malicious_ratio=0.7)

    events = generator.generate(count=count, scenario=scenario)

    if output:
        handler = FileOutputHandler(output, format=log_format)
        handler.write(events)
        console.print(f"[green]✓ Generated {count} logs for {technique_id} to {output}[/green]")
    else:
        handler = StdoutOutputHandler(format=log_format)
        handler.write(events)


@app.command(name="list")
def list_command(
    type: str = typer.Option("scenarios", "--type", "-t", help="List type: scenarios, mitre, generators")
) -> None:
    """List available scenarios, MITRE techniques, or generators."""
    if type == "scenarios":
        table = Table(title="Available Scenarios")
        table.add_column("Generator", style="cyan")
        table.add_column("Scenario", style="magenta")
        table.add_column("Description", style="green")
        table.add_row("auth", "bruteforce", "Multiple failed authentication attempts")
        table.add_row("auth", "successful", "Successful logins")
        table.add_row("firewall", "blocked", "Blocked connections")
        table.add_row("firewall", "portscan", "Port scan detection")
        table.add_row("ids", "alert", "IDS/IPS alerts")
        table.add_row("web", "attack", "Web attacks (SQLi, XSS, etc.)")
        console.print(table)
    elif type == "generators":
        table = Table(title="Available Generators")
        table.add_column("Generator", style="cyan")
        table.add_column("Description", style="green")
        table.add_row("auth", "Authentication and access logs")
        table.add_row("firewall", "Firewall and network logs")
        table.add_row("ids", "IDS/IPS alert logs")
        table.add_row("web", "Web server logs")
        table.add_row("system", "System event logs")
        console.print(table)
    else:
        console.print("[yellow]MITRE technique listing coming soon[/yellow]")


if __name__ == "__main__":
    app()
