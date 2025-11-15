# ChatAds Python SDK

A tiny, dependency-light wrapper around the ChatAds `/v1/chatads/messages` endpoint. It mirrors the response payloads returned by the FastAPI service so you can drop it into CLIs, serverless functions, or orchestration tools.

Learn more at [ChatAds](https://www.getchatads.com).

## Installation

```bash
pip install chatads-sdk
```

The package is published on [PyPI](https://pypi.org/project/chatads-sdk/). Install from source only if you're developing locally.

## Quickstart

```python
from chatads_sdk import ChatAdsClient, AsyncChatAdsClient, FunctionItemPayload

# Synchronous usage
with ChatAdsClient(
    api_key="YOUR_X_API_KEY",
    base_url="https://<your-chatads-domain>",
    raise_on_failure=True,
    max_retries=2,
    retry_backoff_factor=0.75,
) as client:
    payload = FunctionItemPayload(
        message="Looking for a CRM to close more deals",
        ip="1.2.3.4",
        user_agent="Mozilla/5.0",
    )
    result = client.analyze(payload)
    if result.success:
        print(result.data.ad)
    else:
        print(result.error.code, result.error.message)

# Async usage
async with AsyncChatAdsClient(
    api_key="YOUR_X_API_KEY",
    base_url="https://<your-chatads-domain>",
    max_retries=3,
) as async_client:
    result = await async_client.analyze_message("Need data warehousing ideas", country="US")
    print(result.raw)
```

## Error Handling

Non-2xx responses raise `ChatAdsAPIError` and include the parsed error payload plus the original HTTP status code so you can branch on quota/validation failures. Set `raise_on_failure=True` if you want 200 responses with `success=false` to raise the same exception class.

## Notes

- Retries are opt-in. Provide `max_retries>0` to automatically retry transport errors and retryable status codes. The client honors `Retry-After` headers and falls back to exponential backoff.
- `base_url` must point to your HTTPS deployment (the client rejects plaintext URLs so API keys are never transmitted insecurely).
- The default hosted environment lives at `https://chatads--chatads-api-fastapiserver-serve.modal.run`; use your own domain if you're proxying ChatAds behind something else.
- `FunctionItemPayload` matches the server-side `FunctionItem` pydantic model. Keyword arguments passed to `ChatAdsClient.analyze_message()` accept either snake_case (`user_agent`) or camelCase (`userAgent`) keys.
- Reserved payload keys (e.g., `message`, `pageUrl`, `userAgent`) cannot be overridden through `extra_fields`; doing so raises `ValueError` to prevent silent mutations.
- `debug=True` enables structured request/response logging, but payload contents are redacted automatically so you don't leak PII into logs.

## CLI Smoke Test

For a super-quick check, either edit the config block at the top of `run_sdk_smoke.py` or set:

```bash
export CHATADS_API_KEY="..."
export CHATADS_BASE_URL="https://chatads--chatads-api-fastapiserver-serve.modal.run"
export CHATADS_MESSAGE="Looking for ergonomic office chairs"
# Optional extras
export CHATADS_IP="1.2.3.4"
export CHATADS_COUNTRY="US"
```

Then run:

```bash
python run_sdk_smoke.py
```

It prints the raw JSON response or surfaces a `ChatAdsAPIError` with status/error fields so you can see exactly what the API returned.
