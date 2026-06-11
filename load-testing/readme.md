# Load Testing Milestone V1

## Objective

Establish a performance baseline for the Recommendation Service before introducing advanced load testing, deployment automation, or additional recommendation capabilities.

The goal is not to break the system.

The goal is to understand:

* Current latency
* Request throughput
* Error rate
* Cache effectiveness
* Resource utilization

using the existing Docker Compose and monitoring stack.

---

## Directory Structure

load-testing/

├── locustfile.py

├── requirements.txt

├── reports/

│   ├── local/

│   └── aws/

│

└── README.md

---

## Phase 1: Smoke Test

Purpose:

Verify that the Recommendation Service can handle light traffic and that metrics are recorded correctly.

Scenario:

* 10 Virtual Users
* 30 Seconds Duration

Measurements:

* Average Latency
* P95 Latency
* Error Rate
* Request Throughput

Output:

reports/local/smoke-test-report.md

Success Criteria:

* Error Rate = 0%
* P95 Latency < 200ms

---

## Phase 2: Baseline Test

Purpose:

Establish normal operating performance.

Scenario:

* 50 Virtual Users
* 5 Minutes Duration

Measurements:

* Average Latency
* P95 Latency
* Request Throughput
* CPU Usage
* Memory Usage
* Cache Hit Rate

Output:

reports/local/baseline-report.md

Success Criteria:

* Error Rate < 1%
* Stable CPU Usage
* Stable Memory Usage

---

## Phase 3: Cache Benchmark

Purpose:

Measure Redis effectiveness.

Test A:

Random Product Requests

Expected:

* Lower Cache Hit Rate

Test B:

Repeated Hot Product Requests

Expected:

* Higher Cache Hit Rate
* Lower Latency

Measurements:

* Average Latency
* P95 Latency
* Cache Hit Rate

Output:

reports/local/cache-benchmark-report.md

Success Criteria:

Demonstrate measurable latency improvement from Redis caching.

---

## Phase 4: Stress Test

Purpose:

Identify service limits.

Scenarios:

* 100 Virtual Users
* 200 Virtual Users
* 500 Virtual Users

Measurements:

* Error Rate
* P95 Latency
* Throughput
* Resource Utilization

Output:

reports/local/stress-report.md

Success Criteria:

Identify bottlenecks and breaking point.

---

## Deliverables

1. Smoke Test Results
2. Baseline Performance Report
3. Cache Effectiveness Report
4. Stress Test Report
5. Grafana Screenshots
6. Performance Findings
7. Optimization Recommendations

---

## Exit Criteria

Recommendation Service Performance Engineering V1 is complete when:

* Baseline metrics are documented
* Cache effectiveness is measured
* Stress limits are identified
* Performance reports are committed to the repository
* Findings are documented in README.md
