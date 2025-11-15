#!/usr/bin/env python3
"""
Quick sanity check for the published chatads-sdk module.

Edit the CONFIG section and run:

    python run_chatads_module_test.py
"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict

from chatads_sdk import ChatAdsAPIError, ChatAdsClient

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

API_KEY = ""
BASE_URL = "https://chatads--chatads-api-fastapiserver-serve.modal.run"
MESSAGE = "A great home gym set includes bar bells, a bench, and a yoga mat."
CALLER_IP = ""
COUNTRY = "US"
LANGUAGE = "en"


def main() -> int:
    if API_KEY in {"", "YOUR_API_KEY_HERE"}:
        print("Set API_KEY in run_chatads_module_test.py before running.", file=sys.stderr)
        return 2

    client = ChatAdsClient(api_key=API_KEY, base_url=BASE_URL, raise_on_failure=True)

    payload: Dict[str, Any] = {"message": MESSAGE}
    if CALLER_IP:
        payload["ip"] = CALLER_IP
    if COUNTRY:
        payload["country"] = COUNTRY
    if LANGUAGE:
        payload["language"] = LANGUAGE

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
