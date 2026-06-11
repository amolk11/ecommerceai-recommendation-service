# Recommendation Service Performance Baseline V2

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

## Load Configuration

**Virtual Users:** 50

**Spawn Rate:** 10 users/sec

**Duration:** 3 Minutes

**Endpoint:**

GET /api/v1/products/{product_id}/recommendations

**Product ID Used:** 24852

---

## Results

### Request Statistics

**Total Requests:** 7435

**Failures:** 0

**Failure Rate:** 0%

**Requests Per Second (RPS):** 25.4

---

### Latency Metrics

**Average Latency:** 14.44 ms

**Median Latency:** 12 ms

**P95 Latency:** 26 ms

**P99 Latency:** 74 ms

**Maximum Latency:** 207 ms

**Minimum Latency:** 7 ms

---

### Response Characteristics

**Average Response Size:** 2015 bytes

---

## Observations

* Zero request failures observed during execution.
* Service maintained stable throughput throughout the test.
* Average latency remained below 15 ms despite a 5× increase in concurrent users.
* P95 latency improved compared to Baseline V1.
* Tail latency remained well controlled.
* No visible service degradation was observed.
* Recommendation endpoint remained highly responsive under increased concurrency.
* Authentication processing remained stable.
* Redis cache achieved a sustained 100% cache hit rate.
* PostgreSQL and Redis integrations remained healthy during execution.

---

## Initial Assessment

**Status:** PASS ✅

The Recommendation Service demonstrated:

* Excellent scalability characteristics
* Consistent low latency
* Zero request failures
* Stable throughput under increased load
* Effective Redis cache utilization
* Stable authentication performance

This benchmark validates that the current architecture can comfortably support at least 50 concurrent users without measurable performance degradation.

---

## Benchmark Summary

| Metric                | Value      |
| --------------------- | ---------- |
| Users                 | 50         |
| Total Requests        | 7435       |
| RPS                   | 25.4       |
| Average Latency       | 14.44 ms   |
| Median Latency        | 12 ms      |
| P95 Latency           | 26 ms      |
| P99 Latency           | 74 ms      |
| Max Latency           | 207 ms     |
| Min Latency           | 7 ms       |
| Failure Rate          | 0%         |
| Average Response Size | 2015 bytes |

---

## Grafana Metrics Snapshot

### Application Metrics

| Metric                      | Value   |
| --------------------------- | ------- |
| Total Requests              | 10123   |
| Application Average Latency | 1.91 ms |
| Application P95 Latency     | 4.85 ms |
| Cache Hit Rate              | 100%    |
| Authentication Requests     | 10123   |
| Authentication Failures     | 0       |
| Authentication Success Rate | 100%    |

### Observations

* Cache hit rate remained at 100% throughout execution.
* Application latency remained below 5 ms at P95.
* Authentication completed successfully for all requests.
* No cache degradation was observed.
* No infrastructure instability was detected.
* CPU and memory utilization remained stable during the test.

---

## Comparison with Baseline V1

| Metric          | Baseline V1 | Baseline V2 | Change          |
| --------------- | ----------- | ----------- | --------------- |
| Users           | 10          | 50          | +400%           |
| Total Requests  | 2688        | 7435        | +176%           |
| RPS             | 4.8         | 25.4        | +429%           |
| Average Latency | 14.54 ms    | 14.44 ms    | Improved        |
| P95 Latency     | 29 ms       | 26 ms       | Improved        |
| P99 Latency     | 51 ms       | 74 ms       | Slight Increase |
| Failure Rate    | 0%          | 0%          | No Change       |
| Cache Hit Rate  | 100%        | 100%        | No Change       |

---

## Performance Interpretation

The Recommendation Service exhibited near-linear throughput scaling while maintaining stable latency characteristics.

### Key Findings

* Throughput increased significantly with increased concurrency.
* Average latency remained effectively unchanged.
* P95 latency improved despite higher load.
* No errors occurred during execution.
* Redis absorbed the workload effectively through sustained cache hits.
* Authentication introduced no measurable bottleneck.
* No database contention was observed.
* No resource saturation indicators were visible.

The architecture currently demonstrates excellent performance characteristics for the tested workload.

---

## Recommendations

1. Execute a 100-user scalability benchmark.
2. Monitor CPU and memory utilization more closely during higher loads.
3. Introduce mixed product traffic patterns to reduce cache locality.
4. Measure cold-cache versus warm-cache performance.
5. Evaluate database performance under reduced cache effectiveness.
6. Continue incremental load increases until performance degradation is observed.

---

## Next Steps

### Baseline V3

#### Configuration

* Virtual Users: 100
* Spawn Rate: 20 users/sec
* Duration: 3 Minutes

#### Metrics to Capture

* Average Latency
* P95 Latency
* P99 Latency
* Request Throughput (RPS)
* Failure Rate
* CPU Utilization
* Memory Utilization
* Cache Hit Rate

#### Expected Outcome

Determine whether the Recommendation Service continues to scale efficiently under 100 concurrent users and identify the first signs of architectural bottlenecks.

---

## Conclusion

Recommendation Service Baseline V2 was successfully completed.

The service demonstrated:

* Excellent scalability
* Stable latency characteristics
* Zero request failures
* Effective cache utilization
* Reliable authentication performance
* Strong throughput growth under increased concurrency

The current architecture remains healthy and shows no evidence of performance bottlenecks at the tested load level.
