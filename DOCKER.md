# Loggen in Docker

Run **loggen** inside an Alpine-based container with a host directory mounted for the generated logs.

**Image on Docker Hub:** [`sheru/loggen`](https://hub.docker.com/r/sheru/loggen)

---

## 1. Pull the Image

```bash
docker pull sheru/loggen:latest
```

Or pin to a specific version:

```bash
docker pull sheru/loggen:v0.1.0
```

Verify the image is on your machine:

```bash
docker images sheru/loggen
```

> Prefer building from source? See section [Build From Source](#8-build-from-source-alternative) at the bottom.

---

## 2. Prepare the Host Log Directory

Create the directory on your host where generated logs will be written:

```bash
sudo mkdir -p /loggen/fake/log
sudo chown -R $USER:$USER /loggen/fake/log
```

This directory will be mounted into the container at `/logs`. Anything you write to `/logs` inside the container appears in `/loggen/fake/log` on the host.

> The container runs as a non-root user `loggen` with UID/GID 1000, which matches most Linux host users by default. Files created inside the container will be owned by your host user automatically — no `chown` needed afterwards. If your host UID is different from 1000, see the Troubleshooting section below.

---

## 3. Enter the Container

Start an interactive bash session inside the container with the volume mounted:

```bash
docker run -it --rm \
  -v /loggen/fake/log:/logs \
  sheru/loggen:latest
```

You will land in `/logs` inside the container (where files you create show up on the host).

Flags explained:

| Flag | Purpose |
|------|---------|
| `-it` | Interactive TTY (you get a shell) |
| `--rm` | Remove the container when you exit (image is kept) |
| `-v /loggen/fake/log:/logs` | Mount host dir to `/logs` in container |
| `sheru/loggen:latest` | The image to run |

To exit the container: type `exit` or press `Ctrl+D`.

---

## 4. Generate Logs (All 10 Commands)

Once inside the container shell, use any of the commands below. Use `--output <filename>` to save into `/logs` (which appears on the host at `/loggen/fake/log`).

### 4.1 `loggen auth` — Authentication / Access Logs
```bash
loggen auth bruteforce --count 100 --output auth_bruteforce.log
loggen auth successful --count 50 --output auth_successful.log
loggen auth invalid_user --count 30 --output auth_invalid.log
loggen auth privilege_escalation --count 20 --output auth_privesc.log
loggen auth account_lockout --count 15 --output auth_lockout.log
loggen auth default_credentials --count 10 --output auth_defaults.log
```

### 4.2 `loggen firewall` — Firewall / Network Logs
```bash
loggen firewall blocked --count 100 --output fw_blocked.log
loggen firewall portscan --count 50 --output fw_portscan.log
loggen firewall ddos --count 200 --output fw_ddos.log
loggen firewall allowed --count 50 --output fw_allowed.log
loggen firewall unusual_traffic --count 30 --output fw_unusual.log
```

### 4.3 `loggen ids` — IDS / IPS Alerts
```bash
loggen ids alert --count 50 --output ids_alerts.log
loggen ids exploit --count 20 --output ids_exploits.log
loggen ids trojan --count 15 --output ids_trojan.log
loggen ids anomaly --count 25 --output ids_anomaly.log
loggen ids intrusion --count 10 --output ids_intrusion.log
```

### 4.4 `loggen web` — Web Server Logs
```bash
loggen web attack --count 50 --output web_attack.log
loggen web normal --count 100 --output web_normal.log
loggen web scan --count 30 --output web_scan.log
loggen web unauthorized --count 20 --output web_unauthorized.log
loggen web abuse --count 15 --output web_abuse.log
```

### 4.5 `loggen system` — System Event Logs
```bash
loggen system process --count 50 --output sys_process.log
loggen system file --count 40 --output sys_file.log
loggen system registry --count 30 --output sys_registry.log
loggen system service --count 25 --output sys_service.log
loggen system user --count 15 --output sys_user.log
loggen system privilege --count 20 --output sys_privilege.log
```

### 4.6 `loggen dns` — DNS Logs
```bash
loggen dns query --count 100 --output dns_query.log
loggen dns dga --count 50 --output dns_dga.log
loggen dns tunneling --count 20 --output dns_tunneling.log
loggen dns malicious_domain --count 15 --output dns_malicious.log
loggen dns zone_transfer --count 10 --output dns_axfr.log
loggen dns nxdomain --count 30 --output dns_nxdomain.log
```

### 4.7 `loggen email` — Email Server Logs
```bash
loggen email phishing --count 30 --output email_phishing.log
loggen email malware_attachment --count 15 --output email_malware.log
loggen email bec --count 10 --output email_bec.log
loggen email spoofing --count 20 --output email_spoofing.log
loggen email spam --count 50 --output email_spam.log
loggen email normal --count 100 --output email_normal.log
```

### 4.8 `loggen cloud` — Cloud Audit Logs (AWS CloudTrail style)
```bash
loggen cloud console_login --count 30 --output cloud_login.log
loggen cloud iam_changes --count 20 --output cloud_iam.log
loggen cloud bucket_access --count 40 --output cloud_s3.log
loggen cloud key_creation --count 10 --output cloud_keys.log
loggen cloud suspicious_api --count 25 --output cloud_recon.log
loggen cloud resource_changes --count 15 --output cloud_resources.log
```

### 4.9 `loggen mitre` — MITRE ATT&CK Technique-Based Logs
```bash
# Credential Access
loggen mitre T1110.001 --count 50 --output mitre_T1110.001.log    # Brute Force: Password Guessing
loggen mitre T1110.003 --count 50 --output mitre_T1110.003.log    # Brute Force: Password Spraying
loggen mitre T1003 --count 20 --output mitre_T1003.log            # OS Credential Dumping

# Initial Access
loggen mitre T1566.001 --count 30 --output mitre_T1566.001.log    # Spearphishing Attachment
loggen mitre T1566.002 --count 30 --output mitre_T1566.002.log    # Spearphishing Link
loggen mitre T1190 --count 25 --output mitre_T1190.log            # Exploit Public-Facing App
loggen mitre T1078.004 --count 15 --output mitre_T1078.004.log    # Cloud Account Abuse

# Command and Control
loggen mitre T1568.002 --count 40 --output mitre_T1568.002.log    # DGA
loggen mitre T1071.004 --count 20 --output mitre_T1071.004.log    # DNS C2

# Impact
loggen mitre T1499 --count 100 --output mitre_T1499.log           # Endpoint DoS
loggen mitre T1486 --count 30 --output mitre_T1486.log            # Data Encrypted for Impact
```

### 4.10 `loggen list` — Discover Available Options
```bash
loggen list --type generators                       # All 8 generators
loggen list --type scenarios                        # All scenarios per generator
loggen list --type tactics                          # 12 MITRE tactics
loggen list --type mitre                            # All 60 MITRE techniques
loggen list --type mitre --tactic "Credential Access"
loggen list --type mitre --search phishing
```

---

## 5. Output Formats

Every generator command accepts `--format` for the output style:

```bash
loggen auth bruteforce --count 20 --format raw    --output out_raw.log
loggen auth bruteforce --count 20 --format json   --output out.json
loggen auth bruteforce --count 20 --format cef    --output out.cef
loggen auth bruteforce --count 20 --format syslog --output out_syslog.log
```

| Format | Use Case |
|--------|----------|
| `raw` (default) | Human-readable, syslog-like text |
| `json` | SIEM ingestion (Splunk, ELK, etc.) |
| `cef` | Common Event Format (ArcSight, QRadar) |
| `syslog` | Standard RFC 3164 syslog |

---

## 6. One-Shot Runs (No Shell)

If you only need a single command without entering bash, pass it directly to `docker run`:

```bash
docker run --rm \
  -v /loggen/fake/log:/logs \
  sheru/loggen:latest \
  loggen auth bruteforce --count 100 --output auth_attack.log
```

The file appears immediately on the host at `/loggen/fake/log/auth_attack.log`.

---

## 7. Inspecting Logs From the Host

After running any command, view the generated files on the host:

```bash
ls -la /loggen/fake/log/
cat  /loggen/fake/log/auth_bruteforce.log
tail -f /loggen/fake/log/auth_bruteforce.log
```

---

## 8. Build From Source (Alternative)

If you'd rather build the image locally instead of pulling, clone the repo then run:

```bash
docker build -t sheru/loggen:latest .
```

This produces the same image as the one on Docker Hub. The first build takes a few minutes because `pydantic-core` is compiled from source; subsequent builds are cached and fast.

After building, use it exactly the same way as the pulled image (sections 2–7 above).

---

## 9. Releasing a New Version (CI/CD)

A GitHub Actions workflow at [`.github/workflows/docker-publish.yml`](.github/workflows/docker-publish.yml) automatically builds and pushes a **multi-arch** image (`linux/amd64` + `linux/arm64`) to Docker Hub whenever you push a `v*` git tag.

### One-time setup (per GitHub repository)

1. **Create a Docker Hub Personal Access Token**
   - Go to https://app.docker.com/settings/personal-access-tokens
   - Click **Generate new token**, scope **Read & Write**, copy the value.

2. **Add GitHub secrets** in your repo settings → *Settings → Secrets and variables → Actions → New repository secret*:
   - `DOCKERHUB_USERNAME` = `sheru`
   - `DOCKERHUB_TOKEN` = *(paste the token from step 1)*

### Cutting a release

```bash
# Bump version in pyproject.toml first, commit, then:
git tag v0.2.0
git push origin v0.2.0
```

The workflow will:

- Trigger on the `v0.2.0` tag push.
- Build for `linux/amd64` and `linux/arm64`.
- Push the following tags to Docker Hub:
  - `sheru/loggen:0.2.0`
  - `sheru/loggen:0.2`
  - `sheru/loggen:0`
  - `sheru/loggen:v0.2.0`
  - `sheru/loggen:latest`
- Use the GitHub Actions cache for faster subsequent builds.

You can also trigger a build manually from the **Actions** tab → *Build and publish Docker image* → *Run workflow*.

---

## 10. Cleanup

Remove generated logs:
```bash
rm -rf /loggen/fake/log/*
```

Remove the image:
```bash
docker rmi sheru/loggen:latest sheru/loggen:v0.1.0
```

---

## Quick Reference Card

```bash
# Pull once
docker pull sheru/loggen:latest

# Enter the container (interactive)
docker run -it --rm -v /loggen/fake/log:/logs sheru/loggen:latest

# One-shot generation (no shell)
docker run --rm -v /loggen/fake/log:/logs sheru/loggen:latest \
  loggen <generator> <scenario> --count N --output file.log
```

| Generator | Default Scenario |
|-----------|-----------------|
| `auth`     | `bruteforce` |
| `firewall` | `blocked` |
| `ids`      | `alert` |
| `web`      | `attack` |
| `system`   | `process` |
| `dns`      | `query` |
| `email`    | `phishing` |
| `cloud`    | `console_login` |
| `mitre`    | *(requires technique ID)* |
| `list`     | *(no scenario; use `--type`)* |

---

## Troubleshooting

**Permission denied writing to `/logs` (host UID is not 1000)**
The container's `loggen` user is UID/GID 1000. If your host UID differs, either:

1. Make the host directory world-writable:
   ```bash
   chmod 777 /loggen/fake/log
   ```
2. Or override the container user to match yours at runtime:
   ```bash
   docker run -it --rm \
     --user $(id -u):$(id -g) \
     -v /loggen/fake/log:/logs \
     sheru/loggen:latest
   ```
   Check your host UID with `id -u`.

**`docker: command not found`**
Install Docker first: https://docs.docker.com/engine/install/

**Image build fails on Rust compilation (only if building from source)**
The build needs `cargo` and `rust` packages (included in the Dockerfile). If your build host is memory-constrained, increase Docker's resource limits.

**Empty output file**
Make sure you used `--output <filename>` (without `--output`, logs go to stdout instead of the volume-mounted directory).
