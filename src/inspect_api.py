import json
from datetime import datetime, timezone
from pathlib import Path
from socket import timeout

import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_PATH = REPOSITORY_ROOT / "data" / "raw" / "api_snapshot.json"
INVENTORY_PATH = REPOSITORY_ROOT / "docs" / "source_inventory.md"

try:
    response = requests.get(API_URL, timeout=20)    # timeout is set to 20 seconds
    response.raise_for_status()
except requests.RequestException as error:
    raise SystemExit(f"API request failed: {error}") from error     # Handle API request failures

print("status:", response.status_code) # status code of the response
print("content-type:", response.headers.get("Content-Type")) # content type of the response

try:
    payload = response.json()
except ValueError as error:
    raise SystemExit(f"API response was not valid JSON: {error}") from error # Handle JSON decoding errors

print("top-level type:", type(payload).__name__) # top-level type of the payload
if isinstance(payload, list):
    print("record count:", len(payload)) # record count if payload is a list
    print("sample record:", payload[0] if payload else None) # sample record if payload is a list
elif isinstance(payload, dict):
    print("record count:", len(payload)) # record count if payload is a dict
    print("sample record:", payload) # sample record if payload is a dict
else:
    print("record count: unavailable")
    print("sample record:", payload)

with SNAPSHOT_PATH.open("w", encoding="utf-8") as f:    # Write the payload to a JSON file with indentation and UTF-8 encoding
    json.dump(payload, f, indent=2, ensure_ascii=False)

retrieved_at_utc = datetime.now(timezone.utc).isoformat()
print("retrieved_at_utc:", retrieved_at_utc)

inventory = INVENTORY_PATH.read_text(encoding="utf-8") 
timestamp_label = "API retrieval timestamp (UTC):"
timestamp_line = f"{timestamp_label} {retrieved_at_utc}" # Retrieve the current UTC timestamp and format it for the inventory file
if timestamp_label in inventory:
    inventory = "\n".join(
        timestamp_line if line.startswith(timestamp_label) else line
        for line in inventory.split("\n")
    )
else:
    inventory = inventory.rstrip() + f"\n\n## API Retrieval\n\n{timestamp_line}\n"
INVENTORY_PATH.write_text(inventory, encoding="utf-8")
