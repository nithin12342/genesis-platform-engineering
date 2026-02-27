# Custom Metrics Quick Start Guide

This guide helps you quickly integrate custom metrics and SLO tracking into your meta-repository.

## 5-Minute Setup

### Step 1: Install Dependencies

Add to your `requirements.txt` or `pyproject.toml`:

```txt
prometheus-client>=0.19.0
```

### Step 2: Import Metrics

```python
from shared_infrastructure.metrics.custom_metrics import (
    # Choose metrics relevant to your meta-repo
    model_inference_latency,  # For sentinel-ai-engine
    data_pipeline_latency,    # For chronos-data-platform
    service_request_duration, # For titan-microservices-mesh
    security_scan_critical_findings,  # For obsidian-devsecops-platform
    api_endpoint_latency,     # For aurora-fullstack-saas
    SLOTracker
)
```

### Step 3: Expose /metrics Endpoint

**FastAPI:**
```python
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
```

**Flask:**
```python
from flask import Flask, Response
from prometheus_client import generate_latest

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")
```

### Step 4: Record Metrics

**Example: API Latency**
```python
import time

@app.get("/api/data")
def get_data():
    start_time = time.time()
    
    # Your business logic here
    result = fetch_data()
    
    # Record latency
    latency = time.time() - start_time
    api_endpoint_latency.labels(
        endpoint='/api/data',
        method='GET'
    ).observe(latency)
    
    return result
```

**Example: Counter**
```python
from metrics.custom_metrics import user_registration_total

@app.post("/api/register")
def register_user(user_data):
    # Your registration logic
    create_user(user_data)
    
    # Increment counter
    user_registration_total.labels(
        registration_source='web'
    ).inc()
    
    return {"status": "success"}
```

### Step 5: Initialize SLO Tracker

```python
from metrics.custom_metrics import SLOTracker

# Initialize once at application startup
slo_tracker = SLOTracker(
    service_name='my-service',
    slo_definitions={
        'availability': {'target': 0.999, 'window': 30},
        'latency_p99': {'target': 0.1, 'window': 7}
    }
)

# Record SLO metrics
@app.middleware("http")
async def track_slo(request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
        available = response.status_code < 500
        slo_tracker.record_availability(available)
        
        latency = time.time() - start_time
        slo_tracker.record_latency(latency)
        
        return response
    except Exception as e:
        slo_tracker.record_availability(False)
        raise
```

## Metrics by Meta-Repository

### nebula-cloud-platform

```python
from metrics.custom_metrics import (
    gcp_usage_cloud_run_requests,
    gcp_usage_firestore_reads,
    cost_forecast_accuracy,
    infrastructure_cpu_utilization
)

# Record GCP usage
gcp_usage_cloud_run_requests.labels(
    service='my-service',
    region='us-central1'
).set(150000)

# Record cost forecast accuracy
cost_forecast_accuracy.labels(
    forecast_period='30d'
).set(0.96)
```

### sentinel-ai-engine

```python
from metrics.custom_metrics import (
    model_inference_latency,
    model_accuracy,
    model_predictions_total,
    model_drift_detected
)

# Record inference
start = time.time()
prediction = model.predict(input_data)
latency = time.time() - start

model_inference_latency.labels(
    model_name='yolov8',
    model_version='v1.0'
).observe(latency)

model_predictions_total.labels(
    model_name='yolov8',
    model_version='v1.0',
    prediction_type='object_detection'
).inc()

# Record accuracy
model_accuracy.labels(
    model_name='yolov8',
    model_version='v1.0',
    metric_type='precision'
).set(0.95)
```

### chronos-data-platform

```python
from metrics.custom_metrics import (
    airflow_dag_execution_duration,
    data_quality_check_failures,
    records_processed_total,
    data_freshness_lag
)

# Record DAG execution
start = time.time()
run_dag()
duration = time.time() - start

airflow_dag_execution_duration.labels(
    dag_id='daily-etl'
).observe(duration)

# Record data quality
if quality_check_failed:
    data_quality_check_failures.labels(
        check_name='null_check',
        data_source='orders'
    ).inc()

# Record records processed
records_processed_total.labels(
    pipeline_name='daily-etl',
    stage='transform'
).inc(1000000)
```

### titan-microservices-mesh

```python
from metrics.custom_metrics import (
    service_request_duration,
    circuit_breaker_state,
    events_processed_total,
    service_error_rate
)

# Record service request
start = time.time()
response = handle_request()
latency = time.time() - start

service_request_duration.labels(
    service='order-service',
    endpoint='/api/orders',
    method='POST'
).observe(latency)

# Record circuit breaker state
circuit_breaker_state.labels(
    service='order-service',
    dependency='payment-service'
).set(0)  # 0=closed, 1=open, 2=half-open

# Record event processing
events_processed_total.labels(
    event_type='OrderCreated',
    consumer_service='inventory-service'
).inc()
```

### obsidian-devsecops-platform

```python
from metrics.custom_metrics import (
    security_scan_critical_findings,
    security_scan_execution_time,
    policy_violations_total,
    vulnerability_age_days
)

# Record scan results
start = time.time()
scan_results = run_security_scan()
duration = time.time() - start

security_scan_execution_time.labels(
    scanner='checkov',
    resource_type='terraform'
).observe(duration)

security_scan_critical_findings.labels(
    scanner='checkov',
    resource_type='terraform'
).set(scan_results['critical'])

# Record policy violations
if policy_violated:
    policy_violations_total.labels(
        policy_name='require-encryption',
        resource_type='storage'
    ).inc()
```

### aurora-fullstack-saas

```python
from metrics.custom_metrics import (
    user_registration_total,
    api_endpoint_latency,
    websocket_message_latency,
    database_query_duration,
    active_websocket_connections
)

# Record user registration
user_registration_total.labels(
    registration_source='web'
).inc()

# Record API latency
start = time.time()
result = api_handler()
latency = time.time() - start

api_endpoint_latency.labels(
    endpoint='/api/users',
    method='GET'
).observe(latency)

# Record WebSocket connections
active_websocket_connections.labels(
    connection_type='realtime'
).set(len(active_connections))

# Record database query
start = time.time()
db_result = db.query("SELECT * FROM users")
duration = time.time() - start

database_query_duration.labels(
    query_type='SELECT',
    table='users'
).observe(duration)
```

## Common Patterns

### Pattern 1: Timing Operations

```python
import time
from contextlib import contextmanager

@contextmanager
def track_duration(metric, **labels):
    start = time.time()
    try:
        yield
    finally:
        duration = time.time() - start
        metric.labels(**labels).observe(duration)

# Usage
with track_duration(api_endpoint_latency, endpoint='/api/data', method='GET'):
    result = fetch_data()
```

### Pattern 2: Counting Success/Failure

```python
def process_with_metrics(data):
    try:
        result = process_data(data)
        success_counter.labels(operation='process').inc()
        return result
    except Exception as e:
        failure_counter.labels(
            operation='process',
            error_type=type(e).__name__
        ).inc()
        raise
```

### Pattern 3: Tracking Gauge Values

```python
# Update gauge periodically
def update_resource_metrics():
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    
    infrastructure_cpu_utilization.labels(
        resource_type='container',
        resource_name='my-service'
    ).set(cpu_usage)
    
    infrastructure_memory_utilization.labels(
        resource_type='container',
        resource_name='my-service'
    ).set(memory_usage)

# Run periodically (e.g., every 15 seconds)
```

### Pattern 4: SLO Tracking Middleware

```python
from fastapi import Request
import time

@app.middleware("http")
async def slo_tracking_middleware(request: Request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # Record availability
        available = response.status_code < 500
        slo_tracker.record_availability(available, slo_name='availability')
        
        # Record latency
        latency = time.time() - start_time
        slo_tracker.record_latency(latency, slo_name='latency_p99')
        
        # Calculate compliance
        if response.status_code >= 500:
            error_rate = calculate_error_rate()
            slo_tracker.record_error_rate(error_rate, slo_name='error_rate')
        
        return response
        
    except Exception as e:
        slo_tracker.record_availability(False)
        raise
```

## Testing Your Metrics

### 1. Check Metrics Endpoint

```bash
curl http://localhost:8001/metrics
```

Expected output:
```
# HELP model_inference_latency_seconds Time taken for model inference
# TYPE model_inference_latency_seconds histogram
model_inference_latency_seconds_bucket{le="0.01",model_name="yolov8",model_version="v1.0"} 10
model_inference_latency_seconds_bucket{le="0.05",model_name="yolov8",model_version="v1.0"} 45
...
```

### 2. Verify in Prometheus

1. Open http://localhost:9090
2. Go to Graph tab
3. Enter metric name (e.g., `model_inference_latency_seconds`)
4. Click "Execute"
5. Verify data appears

### 3. View in Grafana

1. Open http://localhost:3000
2. Login: admin/admin
3. Go to Dashboards → Browse
4. Open "Business Metrics" dashboard
5. Verify your metrics appear

## Troubleshooting

### Metrics Not Appearing

**Problem:** Metrics don't show up in Prometheus

**Solutions:**
1. Check /metrics endpoint is accessible:
   ```bash
   curl http://localhost:8001/metrics
   ```

2. Verify Prometheus is scraping your service:
   - Open http://localhost:9090/targets
   - Find your service
   - Check if status is "UP"

3. Check Prometheus logs:
   ```bash
   docker logs shared-prometheus
   ```

### High Cardinality Warning

**Problem:** Too many unique label combinations

**Solution:** Avoid using high-cardinality values as labels:
- ❌ Bad: `user_id`, `request_id`, `timestamp`
- ✅ Good: `service`, `endpoint`, `method`, `status_code`

### Metrics Reset on Restart

**Problem:** Counter values reset when service restarts

**Solution:** This is expected behavior. Prometheus handles this with `rate()` and `increase()` functions:
```promql
# Use rate() for counters
rate(user_registration_total[5m])

# Use increase() for total count over time
increase(user_registration_total[1h])
```

## Next Steps

1. **Review full documentation:** See `README.md` for complete details
2. **Explore recording rules:** Check `prometheus/recording-rules.yml`
3. **Configure alerts:** Review `prometheus/alerting-rules.yml`
4. **Customize dashboards:** Edit Grafana dashboards in `grafana/provisioning/dashboards/`
5. **Set SLO targets:** Define appropriate SLOs for your service

## Quick Reference

### Metric Types

- **Counter:** Monotonically increasing value (requests, errors)
- **Gauge:** Value that can go up or down (CPU, memory, connections)
- **Histogram:** Distribution of values (latency, request size)
- **Summary:** Similar to histogram, calculates quantiles

### Common PromQL Queries

```promql
# Request rate (requests per second)
rate(http_requests_total[5m])

# P99 latency
histogram_quantile(0.99, rate(api_endpoint_latency_seconds_bucket[5m]))

# Error rate
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# Availability
sum(rate(http_requests_total{status=~"2.."}[30d])) / sum(rate(http_requests_total[30d]))
```

### Label Best Practices

```python
# ✅ Good: Low cardinality, meaningful labels
metric.labels(
    service='order-service',
    endpoint='/api/orders',
    method='POST',
    status_code='201'
)

# ❌ Bad: High cardinality, not useful for aggregation
metric.labels(
    user_id='12345',
    request_id='abc-def-ghi',
    timestamp='2026-02-01T10:30:00Z'
)
```

## Support

- **Documentation:** `shared-infrastructure/metrics/README.md`
- **Prometheus UI:** http://localhost:9090
- **Grafana UI:** http://localhost:3000
- **Design Doc:** `.kiro/specs/meta-repository-consolidation/design.md`
