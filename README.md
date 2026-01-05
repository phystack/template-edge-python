# Phygrid Edge App Template (Python)

A Python-based edge application template for the Phygrid platform using the `phystack-hub-client` package.

## Features

- **Settings Management**: Get and subscribe to app settings from the platform
- **Event Handling**: Listen for and respond to messages from other twins
- **WebRTC Support**: DataChannel and MediaStream for P2P communication
- **Property Updates**: Report device state back to the platform

## Prerequisites

- Node.js 20+ (for schema generation and CLI tools)
- Python 3.10+
- Docker (for containerized deployment)
- Phystack CLI (`@phystack/cli`)

## Project Structure

```
template-edge-python/
├── src/
│   ├── app.py          # Main Python application
│   └── schema.ts       # Settings schema (TypeScript)
├── meta/
│   └── device.jpg      # App icon
├── package.json        # Node.js config for CLI/schema tools
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container build config
├── settings.json       # Docker container settings
└── tsconfig.json       # TypeScript config for schema
```

## Development

### Install Dependencies

```bash
# Install Node.js dependencies (for schema generation)
yarn install

# Install Python dependencies (for local development)
pip install -r requirements.txt
```

### Define Settings Schema

Edit `src/schema.ts` to define your app's configuration schema:

```typescript
export type Settings = {
  /**
   * @title My Setting
   * @default "default value"
   */
  mySetting: string;

  /**
   * @title Enable Feature
   * @default true
   */
  enableFeature: boolean;
}
```

### Run Locally

```bash
# Set environment variables
export DEVICE_ID="your-device-id"
export ACCESS_KEY="your-access-key"
export PHYHUB_REGION="eu"  # or "us", "au", etc.

# Run the app
python src/app.py
```

## Build & Deploy

### Build the gridapp package

```bash
yarn build
```

This will:
1. Generate settings schema from `src/schema.ts`
2. Copy Python files to `build/`
3. Create the `.gridapp` package

### Publish to Phystack

```bash
yarn pub
```

### Deploy to a device

```bash
yarn deploy
```

## Using the Hub Client

The Python app uses `phystack-hub-client` for platform integration:

```python
from phystack.hub_client import PhyHubClient

# Connect to PhyHub
client = PhyHubClient.from_env()
await client.connect()

# Get edge instance
instance = await client.get_instance()

# Get settings
settings = client.get_settings()

# Subscribe to settings changes
client.on_settings_update(lambda s: print("Settings updated:", s))

# Listen for events
instance.on("message", lambda data, respond: print("Received:", data))

# Emit events to other twins
instance.to(target_twin_id).emit("my-event", {"data": "value"})

# Update reported properties
await instance.update_reported({"status": "running"})

# WebRTC DataChannel
dc = await instance.get_data_channel(peer_twin_id)
dc.send({"message": "hello"})
```

## Docker Build

The app runs in a Docker container based on `python:3.11-slim`:

```bash
# Build locally
docker build -t my-edge-app .

# Run locally
docker run -e DEVICE_ID=xxx -e ACCESS_KEY=xxx -e PHYHUB_REGION=eu my-edge-app
```

## License

MIT
