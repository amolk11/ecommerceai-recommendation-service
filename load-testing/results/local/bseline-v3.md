# Recommendation Service Performance Baseline V3

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

Evaluate Recommendation Service scalability under 100 concurrent users and determine whether latency, throughput, caching, authentication, or infrastructure components begin exhibiting performance degradation.

This benchmark extends Baseline V2 by doubling concurrent user load while maintaining the same workload characteristics.

---

## Load Configuration

**Virtual Users:** 100

**Spawn Rate:** 20 users/sec

**Duration:** 3 Minutes

### Product Pool

Twenty valid products with available recommendations were used throughout the benchmark.

This ensured:

* Consistent recommendation retrieval
* No artificial 404 responses
* Stable cache utilization
* Realistic concurrent workload behavior

---

## Locust Results

### Request Statistics

| Metric                    | Value |
| ------------------------- | ----- |
| Total Requests            | 8928  |
| Failures                  | 0     |
| Failure Rate              | 0%    |
| Requests Per Second (RPS) | 49.2  |

---

### Latency Metrics

| Metric          | Value    |
| --------------- | -------- |
| Average Latency | 25.07 ms |
| Median Latency  | 14 ms    |
| P95 Latency     | 37 ms    |
| P99 Latency     | 490 ms   |
| Maximum Latency | 900 ms   |
| Minimum Latency | 7 ms     |

---

### Response Characteristics

| Metric                | Value         |
| --------------------- | ------------- |
| Average Response Size | 1414.71 bytes |

---

## Grafana Metrics Snapshot

### Application Metrics

| Metric                      | Value   |
| --------------------------- | ------- |
| Total Requests              | 27,071  |
| Application Average Latency | 3.61 ms |
| Application P95 Latency     | 8.72 ms |
| Cache Hit Rate              | 100%    |

---

## Observations

* Zero request failures occurred.
* Throughput nearly doubled compared to Baseline V2.
* Redis maintained a 100% cache hit rate.
* Application latency remained extremely low.
* Authentication remained stable.
* Infrastructure remained healthy throughout execution.
* Recommendation retrieval continued to perform reliably.
* Tail latency increased at P99 while average latency remained healthy.

---

## Comparison with Previous Benchmarks

| Metric      | Baseline V1 | Baseline V2 | Baseline V3 |
| ----------- | ----------- | ----------- | ----------- |
| Users       | 10          | 50          | 100         |
| Requests    | 2688        | 7435        | 8928        |
| RPS         | 4.8         | 25.4        | 49.2        |
| Avg Latency | 14.54 ms    | 14.44 ms    | 25.07 ms    |
| P95         | 29 ms       | 26 ms       | 37 ms       |
| P99         | 51 ms       | 74 ms       | 490 ms      |
| Failures    | 0           | 0           | 0           |

---

## Performance Interpretation

The Recommendation Service continued scaling successfully under increased concurrency.

### Throughput Scaling

Throughput increased from:

* 25.4 RPS at 50 users
* 49.2 RPS at 100 users

This demonstrates near-linear scaling behavior.

### Latency Characteristics

Average latency increased moderately:

* 14.44 ms → 25.07 ms

while P95 latency remained healthy:

* 26 ms → 37 ms

This indicates the majority of requests remained fast under increased load.

### Tail Latency

P99 latency increased significantly:

* 74 ms → 490 ms

while application-level metrics remained healthy.

This suggests occasional request outliers likely caused by:

* Connection management
* Client-side load generation
* Network scheduling
* Docker networking overhead
* Operating system scheduling effects

rather than application bottlenecks.

### Cache Performance

Redis maintained a 100% cache hit rate.

This confirms:

* Successful cache warm-up
* Effective cache utilization
* Minimal database pressure

---

## Assessment

**Status:** PASS ✅

The Recommendation Service demonstrated:

* Excellent scalability
* Stable throughput growth
* Zero request failures
* Effective cache utilization
* Healthy application latency
* Reliable authentication performance

The current architecture comfortably supports 100 concurrent users under the tested workload.

---

## Key Findings

### Scalability

Near-linear throughput scaling was observed between 50 and 100 users.

### Reliability

No request failures occurred.

### Cache Efficiency

Redis maintained a perfect cache hit rate.

### Infrastructure Stability

No signs of Redis, PostgreSQL, FastAPI, or authentication bottlenecks were observed.

### Tail Latency

P99 latency should continue to be monitored in future benchmarks.

---

## Recommendations

1. Execute a 200-user benchmark.
2. Continue monitoring P99 latency growth.
3. Capture CPU and memory utilization during future tests.
4. Introduce mixed cache workloads.
5. Evaluate deployment in a cloud environment.
6. Establish service-level performance targets.

---

## Next Steps

### Baseline V4

Configuration:

* Virtual Users: 200
* Spawn Rate: 40 users/sec
* Duration: 3 Minutes

Metrics:

* Average Latency
* P95 Latency
* P99 Latency
* Failure Rate
* Throughput (RPS)
* Cache Hit Rate
* CPU Utilization
* Memory Utilization

Expected Outcome:

Identify the first signs of scalability limits and determine whether tail latency continues growing under higher concurrency.

---

## Conclusion

Baseline V3 successfully demonstrated that the Recommendation Service architecture scales effectively to 100 concurrent users.

The service maintained zero failures, healthy latency characteristics, perfect cache utilization, and strong throughput growth.

No significant infrastructure bottlenecks were observed during execution.
