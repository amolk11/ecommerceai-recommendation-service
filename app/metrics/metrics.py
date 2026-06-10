from prometheus_client import Counter
from prometheus_client import Histogram


# Request Metrics

REQUEST_COUNT = Counter(
    "recommendation_requests_total",
    "Total recommendation requests",
)

REQUEST_DURATION = Histogram(
    "recommendation_request_duration_seconds",
    "Recommendation request duration",
)


# Cache Metrics

CACHE_HITS = Counter(
    "recommendation_cache_hits_total",
    "Total cache hits",
)

CACHE_MISSES = Counter(
    "recommendation_cache_misses_total",
    "Total cache misses",
)


# Authentication Metrics

AUTH_REQUESTS_TOTAL = Counter(
    "auth_requests_total",
    "Total authentication requests",
)

AUTH_SUCCESS_TOTAL = Counter(
    "auth_success_total",
    "Total successful authentications",
)

AUTH_MISSING_API_KEY_TOTAL = Counter(
    "auth_missing_api_key_total",
    "Requests missing API key",
)

AUTH_INVALID_API_KEY_TOTAL = Counter(
    "auth_invalid_api_key_total",
    "Invalid API key attempts",
)

AUTH_INACTIVE_CLIENT_TOTAL = Counter(
    "auth_inactive_client_total",
    "Inactive client authentication attempts",
)
