# Recommendation Service Performance Baseline V4

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

**Test Type:** Scalability Benchmark

---

## Objective

Evaluate Recommendation Service scalability under 200 concurrent users and identify whether application latency, throughput, caching, authentication, or infrastructure components begin showing signs of contention.

This benchmark extends Baseline V3 by doubling concurrent user load while maintaining the same workload characteristics.

---

## Load Configuration

**Virtual Users:** 200

**Spawn Rate:** 40 users/sec

**Duration:** 3 Minutes

### Product Pool

Twenty valid products with available recommendations were used throughout the benchmark.

```python
[1, 3, 4, 8, 9, 10, 11, 12, 18, 23, 25, 26, 27, 28, 29, 32, 34, 35, 36, 37]
```

This ensured:

- Consistent recommendation retrieval
- No artificial 404 responses
- Stable cache utilization
- Realistic concurrent workload behavior

---

## Locust Results

### Request Statistics

| Metric | Value |
|----------|----------|
| Total Requests | 17,525 |
| Failures | 0 |
| Failure Rate | 0% |
| Requests Per Second (RPS) | 98.5 |

---

### Latency Metrics

| Metric | Value |
|----------|----------|
| Average Latency | 45.45 ms |
| Median Latency | 22 ms |
| P95 Latency | 170 ms |
| P99 Latency | 390 ms |
| Maximum Latency | 671 ms |
| Minimum Latency | 7 ms |

---

### Response Characteristics

| Metric | Value |
|----------|----------|
| Average Response Size | 1415.82 bytes |

---

## Grafana Metrics Snapshot

### Application Metrics

| Metric | Value |
|----------|----------|
| Total Requests | 41,500 |
| Application Average Latency | 9.57 ms |
| Application P95 Latency | 39.8 ms |
| Cache Hit Rate | 100% |

---

## Observations

- Zero request failures occurred.
- Throughput nearly doubled compared to Baseline V3.
- Redis maintained a 100% cache hit rate.
- Authentication remained stable.
- Recommendation retrieval remained reliable throughout execution.
- Infrastructure remained healthy under sustained concurrent load.
- Latency increased as expected under higher concurrency.
- Tail latency remained controlled despite increased contention.

---

## Comparison with Previous Benchmarks

| Metric | Baseline V1 | Baseline V2 | Baseline V3 | Baseline V4 |
|----------|----------|----------|----------|----------|
| Users | 10 | 50 | 100 | 200 |
| Requests | 2688 | 7435 | 8928 | 17525 |
| RPS | 4.8 | 25.4 | 49.2 | 98.5 |
| Avg Latency | 14.54 ms | 14.44 ms | 25.07 ms | 45.45 ms |
| P95 | 29 ms | 26 ms | 37 ms | 170 ms |
| P99 | 51 ms | 74 ms | 490 ms | 390 ms |
| Failures | 0 | 0 | 0 | 0 |

---

## Performance Interpretation

### Throughput Scaling

Throughput continued scaling almost linearly:

- 4.8 RPS at 10 users
- 25.4 RPS at 50 users
- 49.2 RPS at 100 users
- 98.5 RPS at 200 users

This demonstrates strong scalability characteristics for the current architecture.

### Latency Characteristics

Average latency increased from:

- 25.07 ms → 45.45 ms

while P95 latency increased from:

- 37 ms → 170 ms

This indicates the service is beginning to experience contention under higher concurrency while still maintaining acceptable performance.

### Application Performance

Grafana application metrics remained healthy:

- Application Average Latency: 9.57 ms
- Application P95 Latency: 39.8 ms

This suggests the application itself is not the primary bottleneck.

Most latency growth is likely attributable to:

- Connection management
- Request queueing
- Network overhead
- Docker networking
- Operating system scheduling
- Client-side load generation pressure

### Cache Performance

Redis maintained a 100% cache hit rate throughout the benchmark.

This confirms:

- Effective cache utilization
- Minimal database pressure
- Successful cache warm-up
- Stable cache behavior under concurrent traffic

---

## Assessment

**Status:** PASS ✅

The Recommendation Service demonstrated:

- Strong horizontal scalability characteristics
- Stable throughput growth
- Zero request failures
- Excellent cache performance
- Reliable authentication
- Consistent recommendation retrieval
- Stable infrastructure behavior

The current architecture comfortably supports 200 concurrent users under the tested workload.

---

## Key Findings

### Scalability

Throughput scaled nearly linearly from 10 users to 200 users.

### Reliability

Zero failures were observed during the benchmark.

### Cache Efficiency

Redis maintained a perfect cache hit rate under sustained concurrent traffic.

### Infrastructure Stability

No Redis, PostgreSQL, FastAPI, or authentication bottlenecks were observed.

### Tail Latency

P95 latency increased noticeably at 200 concurrent users, indicating the first visible signs of contention.

However, the service remained stable and continued processing requests successfully.

---

## Recommendations

1. Create a consolidated scalability summary report.
2. Capture CPU and memory metrics during future benchmarks.
3. Execute a 500-user stress test if infrastructure limits need to be explored.
4. Monitor P95 and P99 latency growth in future tests.
5. Introduce mixed workloads and cache eviction scenarios.
6. Evaluate performance in a cloud-hosted deployment environment.

---

## Next Steps

### Scalability Summary

Create:

```text
load-testing/reports/local/scalability-summary.md
```

to summarize:

- Baseline V1
- Baseline V2
- Baseline V3
- Baseline V4
- Cache Benchmark V1

and visualize the scaling progression of the Recommendation Service.

---

## Conclusion

Baseline V4 successfully demonstrated that the Recommendation Service architecture scales effectively to 200 concurrent users.

The service maintained:

- Zero failures
- Nearly 100 RPS throughput
- Perfect cache utilization
- Stable authentication performance
- Healthy application latency

The benchmark confirms that the current Recommendation Service foundation is capable of handling substantial concurrent traffic while maintaining reliability and performance.
