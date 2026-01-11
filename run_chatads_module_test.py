#!/usr/bin/env python3
"""
Quick sanity check for the published chatads-sdk module.

Usage:
    # Option 1: Set environment variable
    export CHATADS_API_KEY=your_api_key
    python run_chatads_module_test.py

    # Option 2: Use .env file (create from .env.example)
    python run_chatads_module_test.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

from chatads_sdk import ChatAdsAPIError, ChatAdsClient

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

# Load .env file if it exists
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())

API_KEY = os.environ.get("CHATADS_API_KEY", "")
BASE_URL = os.environ.get("CHATADS_BASE_URL", "https://api.getchatads.com")
MESSAGE = "A great home gym set includes bar bells, a bench, and a yoga mat."

# Optional fields - uncomment and set values if needed
# CALLER_IP = "1.2.3.4"
# COUNTRY = "US"


def main() -> int:
    if not API_KEY:
        print("Set CHATADS_API_KEY env var or create .env file (see .env.example)", file=sys.stderr)
        return 2

    client = ChatAdsClient(api_key=API_KEY, base_url=BASE_URL, raise_on_failure=True)

    payload: Dict[str, Any] = {"message": MESSAGE}

    # Add optional fields if they're defined
    if "CALLER_IP" in globals() and CALLER_IP:
        payload["ip"] = CALLER_IP
    if "COUNTRY" in globals() and COUNTRY:
        payload["country"] = COUNTRY

    try:
        response = client.analyze_message(**payload)
    except ChatAdsAPIError as exc:
        print("ChatAdsAPIError:")
        print(f"  status_code: {exc.status_code}")
        if exc.url:
            print(f"  url: {exc.url}")
        if exc.request_body:
            print("  request:", json.dumps(exc.request_body, indent=2))
        if exc.response:
            print("  raw_response:", json.dumps(exc.response.raw, indent=2))
        return 1
    finally:
        client.close()

    print(json.dumps(response.raw, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
