# Developing Loggen

Notes for maintainers and contributors: building the Docker image from source, doing a multi-arch build locally, and cutting a release.

End-user (Docker Hub) docs live in [DOCKER.md](DOCKER.md). This file is **only** for people who clone the repo.

---

## 1. Build from Source (Single-Arch)

Clone and build:

```bash
git clone git@github.com:sheru-pan/loggen.git
cd loggen
docker build -t sheru/loggen:dev .
```

The first build takes a few minutes because `pydantic-core` (a Rust extension) is compiled from source on Alpine. Subsequent builds are layer-cached and fast.

Test the image locally:

```bash
mkdir -p /tmp/loggen-out
docker run --rm -v /tmp/loggen-out:/logs sheru/loggen:dev \
  loggen auth bruteforce --count 5 --output test.log
cat /tmp/loggen-out/test.log
```

Then use it exactly as documented in [DOCKER.md](DOCKER.md) sections 2–7, just with `sheru/loggen:dev` in place of `sheru/loggen:latest`.

---

## 2. Multi-Arch Build (Local)

The published image on Docker Hub supports `linux/amd64` + `linux/arm64`. To produce the same artifact locally without GitHub Actions:

### One-time setup

```bash
# Register QEMU emulators (needed for cross-arch builds)
docker run --privileged --rm tonistiigi/binfmt --install arm64

# Create a buildx builder that supports multi-platform
docker buildx create --name loggen-multiarch --driver docker-container --use
docker buildx inspect --bootstrap
```

Verify the builder shows both platforms:

```bash
docker buildx ls
# Expect: linux/amd64, linux/arm64 listed under loggen-multiarch
```

### Build and push

```bash
docker login -u sheru   # Docker Hub PAT recommended over password

docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --tag sheru/loggen:latest \
  --tag sheru/loggen:vX.Y.Z \
  --push \
  .
```

Build time on QEMU-emulated arm64 is slow (~15–25 min) because pydantic-core's Rust code recompiles per arch. CI uses the same approach but with build cache, so it's faster on re-runs.

### Verify the manifest

```bash
docker buildx imagetools inspect sheru/loggen:latest
# Should show two platform-specific manifests: linux/amd64 + linux/arm64
```

> Prefer not to do this manually? Use the GitHub Actions release flow in §3 — it's faster and reproducible.

---

## 3. Releasing a New Version (GitHub Actions CI/CD)

A GitHub Actions workflow at [.github/workflows/docker-publish.yml](.github/workflows/docker-publish.yml) automatically builds a multi-arch image and pushes it to Docker Hub whenever a `v*` git tag is pushed to GitHub.

### One-time setup (per repository)

1. **Create a Docker Hub Personal Access Token**
   - https://app.docker.com/settings/personal-access-tokens
   - **Generate new token** → name it (e.g., `github-actions-loggen`), scope **Read & Write**
   - Copy the token value (only shown once)

2. **Add GitHub secrets**
   - Go to *https://github.com/sheru-pan/loggen → Settings → Secrets and variables → Actions → New repository secret*
   - Add `DOCKERHUB_USERNAME` = `sheru`
   - Add `DOCKERHUB_TOKEN` = *(the token from step 1)*

### Cutting a release

```bash
# 1. Bump the version in pyproject.toml
#    Edit version = "0.X.Y"

# 2. Commit the version bump
git add pyproject.toml
git commit -m "Bump version to 0.X.Y"
git push

# 3. Tag and push the tag — this triggers the workflow
git tag v0.X.Y
git push origin v0.X.Y
```

### What the workflow produces

When tag `v0.2.0` is pushed, the workflow publishes these Docker Hub tags pointing at the same multi-arch image:

| Tag | Source |
|-----|--------|
| `sheru/loggen:0.2.0` | semver full |
| `sheru/loggen:0.2`   | semver minor |
| `sheru/loggen:0`     | semver major |
| `sheru/loggen:v0.2.0`| original tag (kept for backwards-compat with v-prefix convention) |
| `sheru/loggen:latest`| only updated for the highest semver tag — won't move backwards if you push `v0.1.5` later |

### Manual trigger (without a tag)

Useful for testing the workflow itself, or rebuilding the same version after a Dockerfile fix:

1. *Repository → Actions → "Build and publish Docker image"*
2. Click **Run workflow** → choose branch → **Run workflow**

When manually dispatched from a branch, the image is tagged with the branch name (e.g., `sheru/loggen:main`).

---

## 4. Project Layout

```
loggen/
├── cli.py                    # Typer CLI entry point + generator registry
├── models/
│   ├── log_event.py         # LogEvent Pydantic model + LogFormat enum
│   └── scenario.py
├── generators/
│   ├── base.py              # BaseGenerator abstract class
│   ├── auth.py              # 6 scenarios
│   ├── firewall.py          # 5 scenarios
│   ├── ids_ips.py           # 5 scenarios
│   ├── web.py               # 5 scenarios
│   ├── system.py            # 6 scenarios
│   ├── dns.py               # 6 scenarios
│   ├── email.py             # 6 scenarios
│   └── cloud.py             # 6 scenarios (AWS CloudTrail style)
├── mitre/
│   ├── techniques.json      # 60 MITRE ATT&CK techniques + generator mapping
│   └── mapper.py            # MitreMapper: lookup, search, filter
├── outputs/
│   ├── file_output.py       # File writer (raw/json/cef/syslog)
│   └── stdout_output.py
└── utils/
    ├── faker_config.py      # FakerProvider: realistic IPs, users, payloads
    ├── timestamps.py        # TimeGenerator: realistic intervals
    └── constants.py         # Log templates
```

### Adding a new generator

1. Create `loggen/generators/<name>.py` extending `BaseGenerator` (see `loggen/generators/dns.py` for a recent example)
2. Implement `generate(count, scenario, **kwargs)` returning `List[LogEvent]`
3. Add a `SCENARIOS` dict mapping scenario name → human description (used by `loggen list`)
4. Register in `GENERATOR_REGISTRY` in `loggen/cli.py` with `(GeneratorClass, default_malicious_ratio)`
5. Add a `@app.command()` function in `loggen/cli.py` calling `_run_generator()`
6. (Optional) Add MITRE technique mappings in `loggen/mitre/techniques.json` pointing to the new generator

### Adding a MITRE technique

Edit `loggen/mitre/techniques.json` and add an entry like:

```json
"T1234.001": {
  "name": "Technique Name",
  "tactic": "Tactic Name",
  "generators": ["generator_name"],
  "scenarios": ["scenario_name"],
  "description": "...",
  "malicious_ratio": 0.7
}
```

No code changes needed — `MitreMapper` loads the JSON at runtime.

---

## 5. Troubleshooting

**Multi-arch build is extremely slow**
The arm64 image is compiled under QEMU emulation. The Rust compile of `pydantic-core` is the slow step. The first build is 15–25 min; subsequent builds reuse the BuildKit cache (or GitHub Actions cache in CI) and are much faster.

**Build fails with "out of memory" during Rust compilation**
Increase Docker's memory limit (Docker Desktop: *Settings → Resources*; Linux daemon: edit cgroup limits) or build one platform at a time:
```bash
docker buildx build --platform linux/amd64 --tag sheru/loggen:test --load .
```

**`docker buildx imagetools inspect` shows `unknown/unknown` entries**
Those are SBOM / attestation manifests added by BuildKit. They're harmless and don't affect runtime. To strip them, the workflow already sets `provenance: false`.

**GitHub Actions cache is stale or huge**
GitHub limits the cache to 10 GB per repo. Old caches are evicted automatically by LRU. To force a clean rebuild, bump the cache key in the workflow or delete caches via *Actions → Caches*.

**Tag was pushed but the workflow didn't trigger**
Check that the tag matches the pattern `v*` in the workflow. Also confirm the tag is pushed to GitHub: `git ls-remote --tags origin`.

**`pyproject.toml` version doesn't match the git tag**
The image tag comes from the git tag, not from `pyproject.toml`. To keep them in sync, always bump `pyproject.toml` in the same commit that precedes the tag.
