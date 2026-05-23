# Loggen - SOC Analyst Training Log Generator

A Python CLI tool that generates realistic, machine-detectable security logs for SOC analyst training. Loggen creates logs mimicking real-world attack scenarios with MITRE ATT&CK technique mapping, making it ideal for hands-on threat detection practice.

## Features

✨ **Multiple Log Types**
- Authentication/Access logs (SSH, system auth)
- Firewall logs (blocked connections, port scans, DDoS)
- IDS/IPS alerts (exploits, malware signatures, anomalies)
- Web server logs (HTTP requests, web attacks)
- System event logs (process creation, file operations, registry changes)

🎯 **MITRE ATT&CK Integration**
- Map techniques to realistic log patterns
- Generate logs for specific techniques (e.g., `loggen mitre T1110.001`)
- Training-focused scenario design

🔧 **Flexible Output**
- Multiple formats: raw text, JSON, CEF, syslog
- Write to files or stdout
- Mix normal baseline traffic with malicious activity (configurable ratio)

📊 **Realistic Data**
- Uses Faker library for authentic usernames, IPs, domains, hostnames
- Realistic timestamps and traffic patterns
- Configurable malicious/benign event distribution (default 20-30%)

## Installation

### Using Virtual Environment (Recommended)

```bash
# Clone or navigate to the project
cd loggen

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in editable mode
pip install -e .
```

### Using pipx

```bash
pipx install -e .
loggen --help
```

## Quick Start

### Generate Auth Logs (Brute Force Attack)

```bash
loggen auth bruteforce --count 20 --output auth_attack.log
```

### Generate Firewall Logs (Port Scan)

```bash
loggen firewall portscan --count 10
```

### Generate Web Attack Logs (JSON Format)

```bash
loggen web attack --count 15 --format json --output web_attacks.json
```

### Generate IDS Alerts

```bash
loggen ids alert --count 5
```

### Generate MITRE ATT&CK Technique Logs

```bash
# T1110.001 - Brute Force: Password Guessing
loggen mitre T1110.001 --count 20

# T1078.001 - Valid Accounts: Default Accounts
loggen mitre T1078.001 --count 10
```

### List Available Scenarios

```bash
loggen list --type scenarios
loggen list --type generators
```

## Usage Guide

### Command Syntax

```bash
loggen <generator> [scenario] [options]
```

### Generators

| Generator | Description | Scenarios |
|-----------|-------------|-----------|
| `auth` | Authentication & access logs | `bruteforce`, `successful`, `invalid_user`, `privilege_escalation`, `account_lockout`, `default_credentials` |
| `firewall` | Firewall & network logs | `blocked`, `portscan`, `ddos`, `allowed`, `unusual_traffic` |
| `ids` | IDS/IPS alert logs | `alert`, `exploit`, `trojan`, `anomaly`, `intrusion` |
| `web` | Web server logs | `attack`, `normal`, `scan`, `unauthorized`, `abuse` |
| `system` | System event logs | `process`, `file`, `registry`, `service`, `user`, `privilege` |
| `mitre` | MITRE ATT&CK techniques | Various (mapped to generators) |

### Options

```bash
--count, -c COUNT           Number of logs to generate (default: 10)
--output, -o PATH          Output file path (default: stdout)
--format, -f FORMAT        Output format: raw, json, cef, syslog (default: raw)
```

### Output Formats

#### Raw (Default)
```
2026-05-23T02:57:51.637517 auth [WARNING] ssh_auth_failure: Failed password for user from 68.96.247.16 port 58542 ssh2
```

#### JSON
```json
{
  "timestamp": "2026-05-23T02:57:51.637517",
  "source": "auth",
  "event_type": "ssh_auth_failure",
  "level": "WARNING",
  "message": "Failed password for user from 68.96.247.16 port 58542 ssh2",
  "fields": {
    "user": "user",
    "source_ip": "68.96.247.16",
    "port": 58542
  }
}
```

#### CEF (Common Event Format)
```
CEF:0|loggen|auth|1.0|ssh_auth_failure|Failed password for user from 68.96.247.16 port 58542 ssh2|5|user=user src_ip=68.96.247.16 port=58542
```

#### Syslog
```
<38>May 23 02:57:51 loggen-host auth[ssh_auth_failure]: Failed password for user from 68.96.247.16 port 58542 ssh2
```

## Examples

### Simulate a Brute Force Attack
```bash
loggen auth bruteforce --count 100 --output scenarios/brute_force.log
```

### Generate DDoS Log Pattern
```bash
loggen firewall ddos --count 50 --format json --output scenarios/ddos_attack.json
```

### Create Web Application Attack Mix
```bash
loggen web attack --count 30 --output scenarios/web_attacks.log
```

### System Privilege Escalation Scenario
```bash
loggen system privilege --count 20 --output scenarios/priv_esc.log
```

### MITRE ATT&CK Training Scenarios

```bash
# Credential Access - Brute Force
loggen mitre T1110.001 --count 25 --output mitre/T1110.001.log

# Initial Access - Valid Accounts
loggen mitre T1078.001 --count 15 --output mitre/T1078.001.log

# Persistence - Privilege Escalation
loggen mitre T1021.006 --count 20 --output mitre/T1021.006.log
```

## Supported MITRE ATT&CK Techniques

- **T1110.001** - Brute Force: Password Guessing
- **T1110.003** - Brute Force: Password Spraying
- **T1078.001** - Valid Accounts: Default Accounts
- **T1021.006** - Remote Services: Windows Remote Management
- **T1021.001** - Remote Services: Remote Terminal Protocol
- **T1040.001** - Traffic Sniffing
- **T1056** - Reconnaissance

## Architecture

```
loggen/
├── models/              # Pydantic data models
│   ├── log_event.py    # LogEvent base model with format support
│   └── scenario.py     # Scenario configuration model
├── generators/          # Log generation modules
│   ├── base.py         # BaseGenerator abstract class
│   ├── auth.py         # Authentication generator
│   ├── firewall.py     # Firewall generator
│   ├── ids_ips.py      # IDS/IPS generator
│   ├── web.py          # Web server generator
│   └── system.py       # System event generator
├── outputs/             # Output handlers
│   ├── base.py         # BaseOutputHandler
│   ├── file_output.py  # File output handler
│   └── stdout_output.py # Stdout handler
├── utils/               # Utilities
│   ├── faker_config.py  # Faker configuration
│   ├── timestamps.py    # Timestamp generation
│   └── constants.py    # Log templates and constants
└── cli.py              # Typer CLI interface
```

## Customization

### Adjusting Malicious Event Ratio

Each generator accepts a `malicious_ratio` parameter (0.0-1.0):

```python
from loggen.generators.auth import AuthGenerator

# 50% malicious events instead of default 20%
generator = AuthGenerator(malicious_ratio=0.5)
events = generator.generate(count=20, scenario="bruteforce")
```

### Adding Custom Log Patterns

Extend any generator:

```python
from loggen.generators.auth import AuthGenerator
from loggen.models.log_event import LogEvent, LogLevel

class CustomAuthGenerator(AuthGenerator):
    def _generate_custom_scenario(self, count: int):
        events = []
        for i in range(count):
            # Custom logic here
            pass
        return events
```

## Testing & Development

Run tests:

```bash
source venv/bin/activate
pytest tests/ -v
```

Run with debugging:

```bash
loggen auth bruteforce --count 5 --format json
```

## Performance

- **Small scenarios** (1-100 logs): < 1 second
- **Medium scenarios** (100-1000 logs): 1-5 seconds
- **Large scenarios** (1000+ logs): Scales linearly

## Known Limitations

- MITRE technique mapping is currently hardcoded (expandable in future)
- SIEM integration (Splunk, ELK) planned for Phase 3
- Configuration file support planned

## Future Enhancements

- [ ] SIEM direct integration (Splunk HEC, Elasticsearch API)
- [ ] Configuration file support (~/.loggen/config.yaml)
- [ ] Extended MITRE technique coverage
- [ ] Custom log template support
- [ ] Scenario replay with seeds
- [ ] Performance profiling & optimization

## Contributing

This is an educational project for SOC analyst training. Contributions welcome for:
- Additional log generators
- More MITRE ATT&CK techniques
- SIEM integrations
- Test coverage

## License

MIT License

## Author

Built for cybersecurity training and threat detection practice.

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check existing documentation
- Review example scenarios

## Disclaimer

This tool generates **simulated logs for training purposes only**. Logs are realistic but not based on real-world attacks. Use responsibly for educational and authorized security testing only.
