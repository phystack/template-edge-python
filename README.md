# template-edge-python

Starter template for PhyStack **EDGE** apps in Python — containerized apps
running on PhyOS devices. Scaffolded by the PhyStack CLI
(`phy app init --type edge --lang python`) or usable directly.

## Getting started

```bash
# Scaffold via the PhyStack CLI
phy app init my-edge-app --type edge --lang python

# Or work directly from this template
bun install                       # dev tooling (schema build)
pip install -r requirements.txt   # Python runtime deps
bun run build
```

## Local development (simulator)

```bash
npm i -g @phystack/device-simulator   # once — provides the phy-simulator binary
phy-simulator start                   # terminal 1: simulated device on :55000
bun run dev                           # terminal 2: `python src/app.py` inside it
```

`bun run dev` runs `phy-simulator run .`, which creates a local twin on the
running simulator and launches the app connected to it. Settings for local
runs are generated into `src/settings/index.json` from the schema defaults
(regenerated automatically; delete the file to reset).

## Flow

```bash
# 1. Edit src/schema.ts (installation settings) and src/app.py (device logic)
# 2. Local build: compile the settings schema and stage the Python sources into build/
bun run build

# 3. Register the app in your tenant (once)
phy app create my-edge-app --type edge

# 4. Log in to your container registry (once)
phy registry login docker.io

# 5. Build + push the image, submit and publish the build
bun run pub
```

`pub` runs `phy app build create $npm_package_name --dir . --push --publish` —
the image ref is derived from your registry login, the pull credential is
attached automatically, and the build is published as soon as it processes.

## Layout

| Path | Purpose |
|------|---------|
| `src/app.py` | App entrypoint (hub-client connection, settings, twin messaging) |
| `src/schema.ts` | Installation-settings schema (TypeScript is used only for schema authoring) |
| `requirements.txt` | Python runtime dependencies (`phystack-hub-client`) |
| `settings.json` | Docker `createOptions` attached to the build |
| `Dockerfile` | Python runtime image |
| `scripts/init-settings.js` | Generates local dev settings from schema defaults |
