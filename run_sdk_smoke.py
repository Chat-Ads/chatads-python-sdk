#!/usr/bin/env python3
"""
Zero-config ChatAds SDK smoke test.

Edit the CONFIG section once (or set env vars), then run:

    python run_sdk_smoke.py
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict

from chatads_sdk import ChatAdsAPIError, ChatAdsClient

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
BASE_URL = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
MESSAGE = "A great home gym set includes bar bells, a bench, and a yoga mat."
CALLER_IP = ""
COUNTRY = "US"
LANGUAGE = "en"

# Retry/strict behavior; tweak as needed.
RAISE_ON_FAILURE = True
MAX_RETRIES = 1
RETRY_BACKOFF_FACTOR = 0.5

def parse_extra_fields(raw: str) -> Dict[str, Any]:
    extra: Dict[str, Any] = {}
    for entry in raw.split(";"):
        entry = entry.strip()
        if not entry:
            continue
        if "=" not in entry:
            raise ValueError(f"Invalid extra field '{entry}'. Expected KEY=VALUE.")
        key, value = entry.split("=", 1)
        extra[key.strip()] = value.strip()
    return extra


def main() -> int:
    if API_KEY == "YOUR_API_KEY_HERE":
        print(
            "Edit API_KEY in run_sdk_smoke.py or set CHATADS_API_KEY before running.",
            file=sys.stderr,
        )
        return 2

    client = ChatAdsClient(
        api_key=API_KEY,
        base_url=BASE_URL,
        raise_on_failure=RAISE_ON_FAILURE,
        max_retries=MAX_RETRIES,
        retry_backoff_factor=RETRY_BACKOFF_FACTOR,
        debug=True,
    )

    request_kwargs = {}
    if CALLER_IP:
        request_kwargs["ip"] = CALLER_IP
    if COUNTRY:
        request_kwargs["country"] = COUNTRY
    if LANGUAGE:
        request_kwargs["language"] = LANGUAGE

    try:
        response = client.analyze_message(
            MESSAGE,
            **request_kwargs,
        )
    except ChatAdsAPIError as exc:
        print("ChatAdsAPIError:", file=sys.stderr)
        print(f"  status_code: {exc.status_code}", file=sys.stderr)
        print("  request:", json.dumps(request_kwargs | {"message": MESSAGE}, indent=2), file=sys.stderr)
        print(f"  url: {client._base_url}{client._endpoint}", file=sys.stderr)
        if exc.response and exc.response.error:
            print(f"  error_code: {exc.response.error.code}", file=sys.stderr)
            print(f"  error_message: {exc.response.error.message}", file=sys.stderr)
        if exc.retry_after:
            print(f"  retry_after: {exc.retry_after}", file=sys.stderr)
        if exc.response:
            print("  raw_response:", json.dumps(exc.response.raw, indent=2), file=sys.stderr)
        return 1
    finally:
        client.close()

    print(json.dumps(response.raw, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
