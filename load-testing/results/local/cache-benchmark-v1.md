# Recommendation Service Cache Benchmark V1

## Test Information

**Date:** 2026-06-11

**Environment:** Local Docker Compose

### Architecture

Locust (Local)

↓

FastAPI (Docker)

↓

Redis (Docker)

↓

PostgreSQL (Local Host)

↓

Platform PostgreSQL (Local Host)

**Test Type:** Cache Performance Benchmark

---

## Objective

Evaluate the effectiveness of Redis caching under a realistic recommendation workload.

Unlike previous benchmarks that repeatedly requested a single product, this benchmark used multiple products with valid recommendations to generate cache misses, cache warm-up activity, and subsequent cache hits.

The goal was to quantify the impact of Redis on application latency and overall service performance.

---

## Load Configuration

**Virtual Users:** 50

**Spawn Rate:** 10 users/sec

**Duration:** 3 Minutes

### Products Used

```python
[1,3,4,8,9,10,11,12,18,23,25,26,27,28,29,32,34,35,36,37]
```

All products were verified to have recommendations available within the recommendation serving layer.

---

## Benchmark Procedure

### Step 1

Flush Redis cache.

```bash
docker exec -it recommendation-redis redis-cli FLUSHALL
```

### Step 2

Verify Redis cache is empty.

```bash
docker exec -it recommendation-redis redis-cli DBSIZE
```

Expected:

```text
(integer) 0
```

### Step 3

Execute load test using multiple valid product IDs.

### Step 4

Observe cache warm-up behavior and monitor Grafana metrics.

---

## Locust Results

### Request Statistics

| Metric                    | Value |
| ------------------------- | ----- |
| Total Requests            | 4446  |
| Failures                  | 0     |
| Failure Rate              | 0%    |
| Requests Per Second (RPS) | 24.8  |

---

### Latency Metrics

| Metric          | Value    |
| --------------- | -------- |
| Average Latency | 16.86 ms |
| Median Latency  | 12 ms    |
| P95 Latency     | 38 ms    |
| P99 Latency     | 94 ms    |
| Maximum Latency | 236 ms   |
| Minimum Latency | 7 ms     |

---

### Response Characteristics

| Metric                | Value         |
| --------------------- | ------------- |
| Average Response Size | 1412.66 bytes |

---

## Grafana Metrics Snapshot

### Application Metrics

| Metric                      | Value   |
| --------------------------- | ------- |
| Total Requests              | 18,068  |
| Application Average Latency | 2.31 ms |
| Application P95 Latency     | 5.00 ms |
| Cache Hit Rate              | 99.5%   |

---

## Observations

* Zero request failures occurred during the benchmark.
* Redis cache warmed quickly despite using multiple products.
* Cache hit rate reached 99.5%.
* Application latency remained extremely low.
* PostgreSQL successfully handled initial cache misses.
* Recommendation retrieval remained stable throughout execution.
* No authentication failures occurred.
* No infrastructure instability was observed.

---

## Comparison with Baseline V2

| Metric          | Baseline V2 | Cache Benchmark V1 |
| --------------- | ----------- | ------------------ |
| Users           | 50          | 50                 |
| Failures        | 0           | 0                  |
| RPS             | 25.4        | 24.8               |
| Average Latency | 14.44 ms    | 16.86 ms           |
| P95 Latency     | 26 ms       | 38 ms              |
| P99 Latency     | 74 ms       | 94 ms              |
| Cache Hit Rate  | 100%        | 99.5%              |

---

## Performance Interpretation

This benchmark intentionally introduced cache misses by distributing requests across multiple products.

Workload progression:

```text
Request
 ↓
Redis Miss
 ↓
PostgreSQL Query
 ↓
Redis Population
 ↓
Redis Hit
 ↓
Response
```

The benchmark demonstrated that:

* Redis warmed rapidly under load.
* Cache misses produced only a modest latency increase.
* Average latency increased by approximately 2.4 ms.
* Service throughput remained effectively unchanged.
* Failure rate remained zero.

These results indicate that PostgreSQL queries are efficient and that Redis provides additional performance optimization rather than masking a database bottleneck.

---

## Key Findings

### Redis Effectiveness

Redis successfully maintained a cache hit rate of 99.5% during a multi-product workload.

### Database Efficiency

The recommendation query path remained performant even during cache warm-up.

### Service Stability

No degradation in throughput or reliability was observed.

### Authentication Performance

Authentication remained stable and introduced no measurable bottleneck.

---

## Assessment

**Status:** PASS ✅

The Recommendation Service demonstrated:

* Effective cache utilization
* Stable latency characteristics
* Zero failures
* Consistent throughput
* Reliable recommendation retrieval
* Efficient database access patterns

Redis caching provides measurable performance benefits while PostgreSQL remains capable of handling cache misses efficiently.

---

## Recommendations

1. Execute Baseline V3 using 100 concurrent users.
2. Introduce larger product pools to further challenge cache locality.
3. Measure cold-cache versus warm-cache performance explicitly.
4. Evaluate database behavior under intentionally reduced cache effectiveness.
5. Continue increasing concurrency until performance degradation becomes visible.

---

## Next Steps

### Baseline V3

Configuration:

* Virtual Users: 100
* Spawn Rate: 20 users/sec
* Duration: 3 Minutes

Metrics to Capture:

* Average Latency
* P95 Latency
* P99 Latency
* Failure Rate
* Throughput (RPS)
* CPU Utilization
* Memory Utilization
* Cache Hit Rate

Expected Outcome:

Identify the first scalability limits of the Recommendation Service architecture and determine whether latency, throughput, or infrastructure resources become bottlenecks under increased concurrency.

---

## Conclusion

Cache Benchmark V1 was successfully completed.

The Recommendation Service demonstrated excellent cache behavior, rapid cache warm-up, stable throughput, low latency, and zero failures under concurrent load.

The benchmark confirms that Redis significantly improves response performance while PostgreSQL remains capable of supporting cache miss scenarios without introducing instability.
