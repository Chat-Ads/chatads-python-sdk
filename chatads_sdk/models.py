"""Dataclasses that mirror the ChatAds Go API request/response models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

FUNCTION_ITEM_OPTIONAL_FIELDS = (
    "ip",
    "country",
    "message_analysis",
    "fill_priority",
    "min_intent",
    "skip_message_analysis",
    "max_offers",
)

_CAMELCASE_ALIASES = {
    "messageanalysis": "message_analysis",
    "fillpriority": "fill_priority",
    "minintent": "min_intent",
    "skipmessageanalysis": "skip_message_analysis",
    "maxoffers": "max_offers",
}

FUNCTION_ITEM_FIELD_ALIASES = {
    **{field: field for field in FUNCTION_ITEM_OPTIONAL_FIELDS},
    **_CAMELCASE_ALIASES,
}

_FIELD_TO_PAYLOAD_KEY = {
    "ip": "ip",
    "country": "country",
    "message_analysis": "message_analysis",
    "fill_priority": "fill_priority",
    "min_intent": "min_intent",
    "skip_message_analysis": "skip_message_analysis",
    "max_offers": "max_offers",
}

RESERVED_PAYLOAD_KEYS = frozenset({"message", *(_FIELD_TO_PAYLOAD_KEY.values())})


@dataclass
class Product:
    """Product metadata from resolution."""
    Title: Optional[str] = None
    Description: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Product"]:
        if not data:
            return None
        return cls(
            Title=data.get("Title"),
            Description=data.get("Description"),
        )


@dataclass
class Offer:
    """Single affiliate offer returned by the API."""
    LinkText: str
    IntentLevel: str
    URL: str
    Status: str
    SearchTerm: Optional[str] = None
    IntentScore: Optional[float] = None
    URLSource: Optional[str] = None
    Reason: Optional[str] = None
    Category: Optional[str] = None
    Product: Optional[Product] = None

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Offer"]:
        if not data:
            return None
        return cls(
            LinkText=data.get("LinkText", ""),
            IntentLevel=data.get("IntentLevel", ""),
            URL=data.get("URL", ""),
            Status=data.get("Status", ""),
            SearchTerm=data.get("SearchTerm"),
            IntentScore=data.get("IntentScore"),
            URLSource=data.get("URLSource"),
            Reason=data.get("Reason"),
            Category=data.get("Category"),
            Product=Product.from_dict(data.get("Product")),
        )


@dataclass
class AnalyzeData:
    """Response data containing affiliate offers."""
    Offers: List[Offer]
    Requested: int
    Returned: int
    LatencyMs: Optional[float] = None
    ExtractionMs: Optional[float] = None
    LookupMs: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["AnalyzeData"]:
        if not data:
            return None
        offers_data = data.get("Offers", [])
        offers = [Offer.from_dict(o) for o in offers_data if o]
        return cls(
            Offers=[o for o in offers if o is not None],
            Requested=int(data.get("Requested", 0)),
            Returned=int(data.get("Returned", 0)),
            LatencyMs=data.get("LatencyMs"),
            ExtractionMs=data.get("ExtractionMs"),
            LookupMs=data.get("LookupMs"),
        )


@dataclass
class ChatAdsError:
    code: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["ChatAdsError"]:
        if not data:
            return None
        return cls(
            code=data.get("code", "UNKNOWN"),
            message=data.get("message", ""),
            details=data.get("details") or {},
        )


@dataclass
class UsageInfo:
    """Usage information returned in API responses."""
    monthly_requests: int
    is_free_tier: bool
    free_tier_limit: Optional[int] = None
    free_tier_remaining: Optional[int] = None
    daily_requests: Optional[int] = None
    daily_limit: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["UsageInfo"]:
        if not data:
            return None
        return cls(
            monthly_requests=int(data.get("monthly_requests") or 0),
            is_free_tier=bool(data.get("is_free_tier", False)),
            free_tier_limit=_maybe_int(data.get("free_tier_limit")),
            free_tier_remaining=_maybe_int(data.get("free_tier_remaining")),
            daily_requests=_maybe_int(data.get("daily_requests")),
            daily_limit=_maybe_int(data.get("daily_limit")),
        )


@dataclass
class ChatAdsMeta:
    """Metadata about the API request and response."""
    request_id: str
    timestamp: Optional[str] = None
    version: Optional[str] = None
    country: Optional[str] = None
    usage: Optional[UsageInfo] = None
    timing_ms: Optional[Dict[str, float]] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> "ChatAdsMeta":
        data = data or {}
        return cls(
            request_id=data.get("request_id", ""),
            timestamp=data.get("timestamp"),
            version=data.get("version"),
            country=data.get("country"),
            usage=UsageInfo.from_dict(data.get("usage")),
            timing_ms=data.get("timing_ms"),
            raw=data,
        )


@dataclass
class ChatAdsResponse:
    success: bool
    meta: ChatAdsMeta
    data: Optional[AnalyzeData] = None
    error: Optional[ChatAdsError] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatAdsResponse":
        data = data or {}
        return cls(
            success=bool(data.get("success", False)),
            data=AnalyzeData.from_dict(data.get("data")),
            error=ChatAdsError.from_dict(data.get("error")),
            meta=ChatAdsMeta.from_dict(data.get("meta")),
            raw=data,
        )


@dataclass
class FunctionItemPayload:
    """Subset of the server's request model.

    Contains all 8 allowed fields per the OpenAPI spec.
    """

    message: str
    ip: Optional[str] = None
    country: Optional[str] = None
    message_analysis: Optional[str] = None
    fill_priority: Optional[str] = None
    min_intent: Optional[str] = None
    skip_message_analysis: Optional[bool] = None
    max_offers: Optional[int] = None
    extra_fields: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload = {"message": self.message}
        for field_name, payload_key in _FIELD_TO_PAYLOAD_KEY.items():
            value = getattr(self, field_name)
            if value is not None:
                payload[payload_key] = value

        conflicts = RESERVED_PAYLOAD_KEYS.intersection(self.extra_fields.keys())
        if conflicts:
            conflict_list = ", ".join(sorted(conflicts))
            raise ValueError(
                f"extra_fields contains reserved keys that would override core payload data: {conflict_list}"
            )
        payload.update(self.extra_fields)
        return payload


def _maybe_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
