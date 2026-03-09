# template-edge-python

Python edge module template for the Phystack platform. Scaffolds a new Python-based edge app with PhyHub connectivity, settings management, and WebRTC support.

## Overview

This repository is a project template consumed by `@phystack/cli` to create new Python edge modules. It provides a working starting point with the `phystack-hub-client` package wired up for settings, event handling, and peer-to-peer communication. The template itself does not deploy anywhere.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Python 3.11, Node.js 20 (schema tooling) |
| Hub client | `phystack-hub-client` |
| Schema | `@phystack/ts-schema` (TypeScript to JSON Schema) |
| Container | Docker (`python:3.11-slim`) |
| CLI | `@phystack/cli` |

## Prerequisites

- Node.js 20+
- Python 3.10+
- Yarn 1.x
- Docker (for container builds)
- Phystack CLI (`@phystack/cli`)

## Getting Started

```bash
cd edge/template-edge-python
yarn install
pip install -r requirements.txt
```

## Project Structure

```
src/
  app.py             # Main Python application
  schema.ts          # Settings schema (TypeScript)
meta/
  device.jpg         # App icon
package.json         # Node.js config for CLI and schema tools
requirements.txt     # Python dependencies
Dockerfile           # Container build definition
settings.json        # Docker container settings
tsconfig.json        # TypeScript config for schema generation
```

## Usage

Scaffold a new Python edge module using the Phystack CLI:

```bash
phy app create --template edge-python my-edge-app
```

The CLI clones this template and replaces placeholder values with the new project name.

### Build and publish workflow

```bash
yarn build           # Generate schema, copy files, package .gridapp
yarn pub             # Publish to Phystack registry
yarn deploy          # Deploy to a target device
```

### Local development

```bash
export DEVICE_ID="your-device-id"
export ACCESS_KEY="your-access-key"
export PHYHUB_REGION="eu"

python src/app.py
```

## Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DEVICE_ID` | Target device identifier | Yes | `d-abc123` |
| `ACCESS_KEY` | Device access key | Yes | `ak-...` |
| `PHYHUB_REGION` | PhyHub region code | Yes | `eu` |

## Testing

No test harness is included in the template. Add a test framework (e.g., `pytest`) after scaffolding.

## Related Documentation

- [`phystack-hub-client` on PyPI](https://pypi.org/project/phystack-hub-client/) -- Python client for PhyHub
- [`@phystack/cli`](https://www.npmjs.com/package/@phystack/cli) -- Phystack command-line interface

## License

MIT
