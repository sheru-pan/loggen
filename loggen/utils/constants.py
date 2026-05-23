"""Constants and templates for log generation."""

# Log message templates
AUTH_MESSAGES = {
    "success": "User {user} logged in from {ip}",
    "failure": "Failed password for {user} from {ip} port {port} ssh2",
    "invalid_user": "Invalid user {user} from {ip} port {port}",
    "sudo": "{user} : TTY=pts/0 ; PWD=/home/{user} ; USER=root ; COMMAND=/bin/bash",
    "lockout": "User {user} account locked due to {count} failed login attempts",
}

FIREWALL_MESSAGES = {
    "blocked": "Blocked {protocol} connection from {src_ip}:{src_port} to {dst_ip}:{dst_port}",
    "allowed": "Allowed {protocol} connection from {src_ip}:{src_port} to {dst_ip}:{dst_port}",
    "port_scan": "Port scan detected from {src_ip} scanning ports {port_range}",
    "ddos": "DDoS attack detected from {src_ip}, {packet_count} packets in {seconds} seconds",
}

IDS_MESSAGES = {
    "alert": "{signature} detected from {src_ip} to {dst_ip}",
    "exploit": "Exploit {cve} detected in traffic from {src_ip}",
    "trojan": "Trojan activity signature match: {family} from {src_ip}",
    "anomaly": "Network anomaly detected: {type} from {src_ip}",
}

WEB_MESSAGES = {
    "request": "{method} {path} {status} {bytes} from {user_agent}",
    "sql_injection": "SQL injection attempt detected in parameter {param}",
    "xss": "XSS payload detected in {location}",
    "path_traversal": "Path traversal attempt: {path}",
    "command_injection": "Command injection attempt detected",
    "unauthorized": "Unauthorized access attempt to {resource} by {user}",
}

SYSTEM_MESSAGES = {
    "process_creation": "New process created: {process} (PID: {pid}) by user {user}",
    "file_creation": "File created: {file_path} by user {user}",
    "registry_modification": "Registry key modified: {key} by user {user}",
    "service_start": "Service {service_name} started by user {user}",
    "user_creation": "User account created: {username}",
    "privilege_escalation": "Privilege escalation attempt by {user} to {target_user}",
}

ATTACK_PATTERNS = {
    "brute_force": "Multiple failed authentication attempts",
    "privilege_escalation": "Attempt to gain elevated privileges",
    "lateral_movement": "Suspicious internal network activity",
    "data_exfiltration": "Large data transfer to external IP",
    "malware_execution": "Suspicious process or file execution",
    "credential_theft": "Credential harvesting activity",
    "c2_communication": "Command and control communication",
}

CEF_FIELDS = {
    "src": "Source IP",
    "dst": "Destination IP",
    "spt": "Source Port",
    "dpt": "Destination Port",
    "proto": "Protocol",
    "act": "Action",
    "msg": "Message",
}

COMMON_PORTS = {
    "ssh": 22,
    "telnet": 23,
    "http": 80,
    "https": 443,
    "dns": 53,
    "smtp": 25,
    "mysql": 3306,
    "postgres": 5432,
    "rdp": 3389,
    "vnc": 5900,
}

MITRE_TACTICS = [
    "Reconnaissance",
    "Resource Development",
    "Initial Access",
    "Execution",
    "Persistence",
    "Privilege Escalation",
    "Defense Evasion",
    "Credential Access",
    "Discovery",
    "Lateral Movement",
    "Collection",
    "Command and Control",
    "Exfiltration",
    "Impact",
]

HTTP_ATTACK_PATHS = [
    "/admin.php",
    "/wp-admin/",
    "/login.aspx",
    "/../../../etc/passwd",
    "/search.php?q=<script>",
    "/api/users?id=1' OR '1'='1",
    "/upload.php",
    "/shell.aspx",
]
