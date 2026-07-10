# CLAUDE.md — template-edge-python

Starter template for PhyStack **EDGE** apps in Python: containerized apps
that run on PhyOS devices and talk to the platform through
`phystack-hub-client` (an Edge twin). Scaffolded by
`phy app init <name> --type edge --lang python`.

## Commands (bun for tooling, python for the app)

| Command | What it runs |
|---|---|
| `bun install` | Dev tooling (`ts-schema`, TypeScript) |
| `pip install -r requirements.txt` | Python runtime dependencies |
| `bun run dev` | `phy-simulator run . --dev-command 'python src/app.py'` — local simulated device + the app inside it |
| `bun run start` | `python src/app.py` — run the app directly |
| `bun run build` | Compile `src/schema.ts` to `build/`, copy `src/*.py` + `requirements.txt` into `build/`, `touch build/index.html` |
| `bun run pub` | `bun run build && phy app build create $npm_package_name --dir . --push --publish` |

Note: `src/schema.ts` is TypeScript **only for schema authoring** — the app
itself is pure Python. `bun run build` stages files; it does not build a
container (that happens in `pub` via the CLI).

## Dev loop

- `bun run dev` needs the standalone simulator installed once:
  `npm i -g @phystack/device-simulator` (provides the `phy-simulator`
  binary). It boots a simulated device on `:55000` and runs the app
  against it.
- The `predev` hook generates `src/settings/index.json` from the schema
  defaults — a local-dev bootstrap only; delete it to regenerate. In
  production, settings arrive on the Edge twin's desired properties.

## Publish flow (new `phy` CLI grammar)

```bash
phy login
phy app create <name> --type edge   # register in your tenant (once)
phy registry login docker.io        # container registry credentials (once)
bun run pub                         # build + push image, submit + publish build
```

The legacy `@phystack/cli` (Node) does not work with this template — use the
Rust `phy` CLI only.

## Layout

| Path | Purpose |
|---|---|
| `src/app.py` | Entrypoint — hub-client connection, settings handling, twin messaging |
| `src/schema.ts` | Installation-settings schema source (→ `build/schema.json` + `meta-schema.json`) |
| `requirements.txt` | Python runtime dependencies (`phystack-hub-client`) |
| `settings.json` | Docker `createOptions` (HostConfig) attached to the build |
| `Dockerfile` | Python runtime image |
| `scripts/init-settings.js` | Generates local dev settings from schema defaults |

## Gotchas

- `application-type` in package.json must stay `edge` — the CLI validates it
  on `phy app build create`.
- The package.json `name` is the app name used by `pub`
  (`$npm_package_name`); `phy app init` patches it on scaffold.
- Keep this template in step with `template-edge` (Node) where the schema
  pipeline and simulator flow are concerned — only the app runtime differs.
