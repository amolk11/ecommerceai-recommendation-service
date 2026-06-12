# Recommendation Service Database Benchmark V1

## Test Information

**Date:** 2026-06-12

**Environment:** Local Docker Compose

### Architecture

Locust (Local)

↓

FastAPI (Docker)

↓

Redis (Docker - Disabled)

↓

PostgreSQL (Local Host)

↓

Platform PostgreSQL (Local Host)

**Test Type:** Database Benchmark

**Objective:** Measure Recommendation Service performance with Redis caching disabled and quantify the impact of direct PostgreSQL recommendation retrieval.

---

## Benchmark Configuration

### Cache Configuration

```text
CACHE_ENABLED=false
```

### Load Configuration

| Parameter               | Value        |
| ----------------------- | ------------ |
| Virtual Users           | 200          |
| Spawn Rate              | 40 users/sec |
| Duration                | 3 Minutes    |
| Cache                   | Disabled     |
| Authentication          | Enabled      |
| Recommendation Endpoint | Enabled      |

---

## Endpoint Tested

```http
GET /api/v1/products/{product_id}/recommendations
```

---

## Locust Results

### Request Statistics

| Metric                    | Value  |
| ------------------------- | ------ |
| Total Requests            | 15,034 |
| Failures                  | 0      |
| Failure Rate              | 0%     |
| Requests Per Second (RPS) | 81.4   |

---

### Latency Metrics

| Metric          | Value     |
| --------------- | --------- |
| Average Latency | 386.54 ms |
| Median Latency  | 370 ms    |
| P95 Latency     | 790 ms    |
| P99 Latency     | 1000 ms   |
| Maximum Latency | 1275 ms   |
| Minimum Latency | 10 ms     |

---

### Response Characteristics

| Metric                | Value         |
| --------------------- | ------------- |
| Average Response Size | 1419.27 bytes |

---

## Grafana Metrics Snapshot

### Application Performance

| Metric                      | Value  |
| --------------------------- | ------ |
| Total Requests              | 14,465 |
| Application Average Latency | 188 ms |
| Application P95 Latency     | 467 ms |
| Cache Hit Rate              | 0%     |

---

## Observations

* Redis caching was fully disabled.
* Cache hit rate remained at 0% throughout the benchmark.
* All recommendation requests were served directly from PostgreSQL.
* Authentication remained stable during execution.
* No request failures were observed.
* PostgreSQL successfully handled sustained concurrent traffic.
* Throughput remained stable throughout execution.
* Recommendation retrieval remained reliable despite the absence of Redis.
* Application behavior remained stable under concurrent load.

---

## Cache Validation

The benchmark successfully verified that Redis was bypassed.

### Evidence

| Metric           | Value |
| ---------------- | ----- |
| Cache Enabled    | False |
| Cache Hit Rate   | 0%    |
| Request Failures | 0%    |

This confirms that all recommendation requests were processed using direct PostgreSQL access.

---

## Comparison With Cached Execution

### Baseline V4 (Cache Enabled)

| Metric          | Value    |
| --------------- | -------- |
| Users           | 200      |
| RPS             | 98.5     |
| Average Latency | 45.45 ms |
| Median Latency  | 22 ms    |
| P95 Latency     | 170 ms   |
| P99 Latency     | 390 ms   |
| Max Latency     | 671 ms   |
| Failure Rate    | 0%       |

### Database Benchmark V1 (Cache Disabled)

| Metric          | Value     |
| --------------- | --------- |
| Users           | 200       |
| RPS             | 81.4      |
| Average Latency | 386.54 ms |
| Median Latency  | 370 ms    |
| P95 Latency     | 790 ms    |
| P99 Latency     | 1000 ms   |
| Max Latency     | 1275 ms   |
| Failure Rate    | 0%        |

---

## Redis Impact Analysis

### Average Latency

```text
45.45 ms
↓
386.54 ms
```

Redis reduced average latency by approximately **8.5x**.

### Median Latency

```text
22 ms
↓
370 ms
```

Redis reduced median latency by approximately **16.8x**.

### P95 Latency

```text
170 ms
↓
790 ms
```

Redis reduced P95 latency by approximately **4.6x**.

### Throughput

```text
98.5 RPS
↓
81.4 RPS
```

Redis improved throughput by approximately **21%**.

---

## Engineering Findings

### Redis Provides Significant Performance Benefits

The benchmark demonstrates that Redis substantially improves recommendation retrieval latency and overall system responsiveness.

### PostgreSQL Remains Stable

Despite Redis being disabled:

* Zero failures occurred.
* Authentication remained stable.
* Recommendation retrieval continued functioning correctly.
* PostgreSQL sustained the workload successfully.

### Cache Layer Is a Critical Scalability Component

Redis is not merely an optimization layer.

The benchmark demonstrates that Redis significantly reduces:

* Average latency
* Median latency
* Tail latency (P95 / P99)
* Database workload

while improving throughput under concurrent traffic.

---

## Assessment

### Status

✅ PASS

The Recommendation Service successfully handled a 200-user workload with Redis disabled.

The benchmark confirms:

* Reliable PostgreSQL performance
* Stable application behavior
* Successful authentication handling
* Zero request failures
* Measurable performance gains from Redis caching

---

## Key Takeaways

1. Redis reduced average latency by more than 8x.
2. Redis significantly improved P95 and P99 latency.
3. PostgreSQL remained stable under concurrent load.
4. Recommendation retrieval continued functioning without cache support.
5. Redis is a critical component for achieving low-latency recommendation serving.
6. The current architecture demonstrates strong resilience under cache-disabled conditions.

---

## Recommendations

1. Maintain Redis as a mandatory production component.
2. Continue monitoring cache hit rate as a primary performance indicator.
3. Investigate PostgreSQL query optimization opportunities for cache-disabled scenarios.
4. Introduce recommendation pre-warming strategies for high-demand products.
5. Benchmark future recommendation models against this database-only baseline.

---

## Conclusion

Database Benchmark V1 successfully quantified the value of Redis within the Recommendation Service architecture.

The service remained reliable and failure-free without caching, while Redis demonstrated substantial improvements in latency and throughput. This benchmark validates the architectural decision to include Redis as a core performance layer within the CommerceAI Recommendation Service.
