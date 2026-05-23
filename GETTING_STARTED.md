# Getting Started with Loggen

## What is Loggen?

Loggen is a CLI tool for generating realistic security logs for SOC analyst training. It simulates real-world attack scenarios with configurable malicious/benign event distributions, helping you practice threat detection.

## Installation (5 minutes)

```bash
# Navigate to project
cd /home/sheru/Documents/SOC/RESEARCH/PROJECTS/loggen

# Activate virtual environment
source venv/bin/activate

# Loggen is already installed! Test it:
loggen --help
```

## First Steps (Beginner)

### 1. Generate Your First Logs

```bash
# Simple auth brute force scenario
loggen auth bruteforce --count 20
```

### 2. Output to a File

```bash
# Save to file
loggen auth bruteforce --count 50 --output my_logs.log

# View them
cat my_logs.log
```

### 3. Try Different Log Types

```bash
# Web attacks
loggen web attack --count 10

# Firewall blocking
loggen firewall blocked --count 15

# IDS alerts
loggen ids alert --count 5
```

## Practical Scenarios (Intermediate)

### Scenario 1: Detect a Brute Force Attack
```bash
# Generate 100 failed auth attempts from same IP
loggen auth bruteforce --count 100 --output scenario1.log

# Review the logs - notice:
# - Same source IP attacking one target user
# - Failed passwords in rapid succession
# - Increasing port numbers
```

### Scenario 2: Network Reconnaissance
```bash
# Port scan detection
loggen firewall portscan --count 20 --format json --output scenario2.json

# Review as JSON - notice:
# - Sequential port numbers (22, 80, 443, 3389, etc.)
# - Single attacker IP
# - Multiple target ports
```

### Scenario 3: Web Application Attack
```bash
# Mix of SQL injection, XSS, path traversal
loggen web attack --count 30 --output scenario3.log

# Look for:
# - SQL injection payloads: ' OR '1'='1
# - XSS attempts: <script>, onerror=
# - Path traversal: ../../../etc/passwd
```

## Advanced Usage (Expert)

### 1. MITRE ATT&CK Training

Generate logs for specific attack techniques:

```bash
# T1110.001 - Credential Access / Brute Force
loggen mitre T1110.001 --count 50 --output T1110.001.log

# T1078.001 - Initial Access / Valid Accounts (default creds)
loggen mitre T1078.001 --count 30 --output T1078.001.log

# T1021.006 - Privilege Escalation
loggen mitre T1021.006 --count 20 --output T1021.006.log
```

### 2. Different Output Formats

```bash
# Raw format (default)
loggen auth successful --count 5 --format raw

# JSON - great for log aggregation tools
loggen auth successful --count 5 --format json

# CEF (Common Event Format) - industry standard
loggen auth successful --count 5 --format cef

# Syslog format
loggen auth successful --count 5 --format syslog
```

### 3. Bulk Scenario Generation

Create a training dataset:

```bash
# Create scenarios directory
mkdir -p scenarios/credentials_access

# Generate multiple MITRE techniques for this tactic
loggen mitre T1110.001 --count 100 --output scenarios/credentials_access/T1110.001.log
loggen mitre T1110.003 --count 100 --output scenarios/credentials_access/T1110.003.log
loggen mitre T1078.001 --count 100 --output scenarios/credentials_access/T1078.001.log

# Now you have a full training dataset for credential access techniques
```

### 4. List All Available Options

```bash
# See all available scenarios
loggen list --type scenarios

# See all generators
loggen list --type generators
```

## Training Exercises

### Exercise 1: Spot the Attack
Generate mixed logs and find the attack:
```bash
# Generate 80% normal + 20% attack
loggen auth successful --count 80 --output exercise1.log
loggen auth bruteforce --count 20 --output >> exercise1.log
# Shuffle the lines manually or sort by timestamp
```

### Exercise 2: Analyze Attack Chain
Simulate multi-stage attack:
```bash
# Initial reconnaissance
loggen firewall portscan --count 10 --output attack_chain.log

# Exploitation attempt
loggen web attack --count 10 --output >> attack_chain.log

# Post-exploitation
loggen system privilege --count 10 --output >> attack_chain.log

# Analyze the chain chronologically
```

### Exercise 3: Build Your SIEM Dashboard
Generate logs in JSON for your SIEM practice:
```bash
loggen auth bruteforce --count 100 --format json --output siem_auth.json
loggen firewall blocked --count 50 --format json --output siem_firewall.json
loggen ids alert --count 30 --format json --output siem_ids.json

# These can be imported into your SIEM training environment
```

## Common Commands

```bash
# Auth scenarios
loggen auth bruteforce --count 50          # Failed login attempts
loggen auth successful --count 50          # Normal logins
loggen auth invalid_user --count 30        # Non-existent user attempts
loggen auth privilege_escalation --count 20 # sudo/privilege escalation
loggen auth account_lockout --count 10     # Account lockout events
loggen auth default_credentials --count 15 # Default account usage

# Firewall scenarios
loggen firewall blocked --count 50         # Blocked connections
loggen firewall portscan --count 30        # Port scanning
loggen firewall ddos --count 100           # DDoS traffic
loggen firewall allowed --count 50         # Normal allowed traffic
loggen firewall unusual_traffic --count 20 # Suspicious patterns

# IDS scenarios
loggen ids alert --count 50                # Generic alerts
loggen ids exploit --count 20              # Exploit detection
loggen ids trojan --count 15               # Malware signatures
loggen ids anomaly --count 25              # Anomaly detection
loggen ids intrusion --count 10            # Intrusion attempts

# Web scenarios
loggen web attack --count 50               # Web attacks
loggen web normal --count 50               # Normal traffic
loggen web scan --count 30                 # Vulnerability scanning
loggen web unauthorized --count 20         # Auth failures
loggen web abuse --count 15                # Rate limiting/abuse

# System scenarios
loggen system process --count 50           # Process creation
loggen system file --count 40              # File operations
loggen system registry --count 30          # Registry changes (Windows)
loggen system service --count 25           # Service events
loggen system user --count 15              # User management
loggen system privilege --count 20         # Privilege escalation
```

## Tips for SOC Training

1. **Start Small**: Generate 10-20 logs at first, understand the pattern
2. **Read the Messages**: Loggen's messages contain actual attack indicators
3. **Mix Scenarios**: Combine normal and attack logs to practice filtering
4. **Export to JSON**: Use JSON format for integration with other tools
5. **Time-Based Analysis**: Notice the timestamps tell a story of the attack
6. **Use Different Formats**: Practice reading CEF and syslog formats

## Next Steps

1. ✅ Run basic commands from "First Steps"
2. ✅ Work through "Practical Scenarios"
3. ✅ Try "Advanced Usage" with MITRE techniques
4. ✅ Complete "Training Exercises"
5. 🔄 Build your own custom scenarios
6. 🔄 Integrate with your SIEM training environment

## Troubleshooting

### Command not found
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall if needed
pip install -e .
```

### File permission errors
```bash
# Ensure output directory exists
mkdir -p output_directory
loggen auth bruteforce --output output_directory/logs.log
```

### Want more help?
```bash
# Detailed help for any command
loggen auth --help
loggen firewall --help
loggen mitre --help
```

## Happy Hunting! 🎯

Use Loggen to build your threat detection muscles. Start with obvious attacks, then work toward finding subtle indicators in noisy datasets.
