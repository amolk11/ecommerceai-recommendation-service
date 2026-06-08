from prometheus_client import Counter
from prometheus_client import Histogram


REQUEST_COUNT = Counter(
    "recommendation_requests_total",
    "Total recommendation requests",
)

CACHE_HITS = Counter(
    "recommendation_cache_hits_total",
    "Total cache hits",
)

CACHE_MISSES = Counter(
    "recommendation_cache_misses_total",
    "Total cache misses",
)

REQUEST_DURATION = Histogram(
    "recommendation_request_duration_seconds",
    "Recommendation request duration",
)