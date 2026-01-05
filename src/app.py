#!/usr/bin/env python3
"""
Phygrid Edge App Template (Python)

This template demonstrates how to create a Python-based edge app
using the phystack-hub-client package.
"""

import asyncio
import json
import signal
import sys
from typing import Any, Optional

from phystack.hub_client import PhyHubClient


async def main() -> None:
    """Main application entry point."""
    print("Starting Phygrid Edge App (Python)...")

    # Connect to PhyHub
    client = PhyHubClient.from_env()
    await client.connect()

    print(f"Connected to PhyHub")

    # Get edge instance
    instance = await client.get_instance()
    if not instance:
        print("Error: Could not get edge instance")
        await client.disconnect()
        return

    print(f"Edge instance ID: {instance.id}")

    # Get settings
    settings = client.get_settings()
    print(f"Settings: {json.dumps(settings, indent=2)}")

    # Subscribe to settings updates
    def on_settings_update(new_settings: dict[str, Any]) -> None:
        print(f"Settings updated: {json.dumps(new_settings, indent=2)}")

    client.on_settings_update(on_settings_update)

    # Listen for incoming messages
    def on_message(data: Any, respond: Optional[Any] = None) -> None:
        print(f"Received message: {data}")
        if respond:
            respond({"status": "ok", "received": data})

    instance.on("message", on_message)

    # Example: periodic task
    counter = 0

    async def periodic_task() -> None:
        nonlocal counter
        while True:
            counter += 1
            print(f"Hello, world! Counter: {counter}")
            print(f"Current settings: {json.dumps(settings, indent=2)}")

            # Example: emit an event to subscribers
            # instance.emit("status", {"counter": counter})

            await asyncio.sleep(3)

    # Handle graceful shutdown
    shutdown_event = asyncio.Event()

    def signal_handler(sig: int, frame: Any) -> None:
        print(f"\nReceived signal {sig}, shutting down...")
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Run periodic task until shutdown
    periodic = asyncio.create_task(periodic_task())

    try:
        await shutdown_event.wait()
    finally:
        periodic.cancel()
        try:
            await periodic
        except asyncio.CancelledError:
            pass
        await client.disconnect()
        print("Disconnected from PhyHub")


if __name__ == "__main__":
    asyncio.run(main())
