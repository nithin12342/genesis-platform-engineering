# Custom Metrics and SLO Tracking

This directory contains custom business-specific metrics and SLO (Service Level Objective) tracking infrastructure for all meta-repositories in the consolidation project.

## Overview

The metrics system provides:
- **Business-specific metrics** tailored to each meta-repository
- **SLO tracking** with automated compliance monitoring
- **Prometheus recording rules** for efficient metric aggregation
- **Alerting rules** for SLO violations and threshold breaches
- **Grafana dashboards** for visualization

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Meta-Repositories                         │
│  (nebula, sentinel, chronos, titan, obsidian, aurora)       │
└────────────────┬────────────────────────────────────────────┘
                 │ Expose /metrics endpoint
                 ▼
┌─────────────────────────────────────────────────────────────┐
│                      Prometheus                              │
│  - Scrapes metrics every 15s                                 │
│  - Evaluates recording rules every 30s                       │
│  - Evaluates alerting rules every 1m                         │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ├──► Recording Rules (pre-compute SLO metrics)
                 ├──► Alerting Rules (trigger on violations)
                 └──► Grafana (visualization)
```

## Metrics by Meta-Repository

### 1. nebula-cloud-platform (Infrastructure & Cost)

**Business Metrics:**
- `gcp_usage_cloud_run_requests` - Cloud Run requests vs 2M free tier limit
- `gcp_usage_firestore_reads` - Firestore reads vs 50k/day limit
- `gcp_usage_firestore_writes` - Firestore writes vs 20k/day limit
- `gcp_usage_firestore_storage` - Firestore storage vs 1GB limit
- `gcp_usage_cloud_storage` - Cloud Storage vs 5GB limit
- `gcp_cost_by_service` - Estimated monthly cost by service
- `cost_forecast_accuracy` - Cost forecasting model accuracy
- `infrastructure_cpu_utilization` - CPU utilization by resource
- `infrastructure_memory_utilization` - Memory utilization by resource
- `infrastructure_deployment_duration` - Infrastructure deployment time
- `infrastructure_drift_detected` - Infrastructure drift detection

**SLOs:**
- API Availability: 99.9% (30-day window)
- API Latency P99: 100ms (7-day window)
- Cost Forecast Accuracy: 95% (30-day window)

**Recording Rules:**
- `nebula:api:availability:ratio_30d` - 30-day API availability
- `nebula:api:latency:p99_7d` - 7-day P99 latency
- `nebula:gcp:*:usage_percentage` - GCP free tier usage percentages

### 2. sentinel-ai-engine (MLOps & AI)

**Business Metrics:**
- `model_training_duration_seconds` - Model training time
- `model_inference_latency_seconds` - Inference latency
- `model_accuracy` - Model accuracy by type (precision, recall, f1)
- `model_predictions_total` - Total predictions made
- `model_drift_detected` - Model drift detection flag
- `model_training_failures_total` - Training failure count
- `model_data_quality_score` - Training data quality
- `model_feature_importance` - Feature importance scores
- `model_prediction_confidence` - Prediction confidence distribution

**SLOs:**
- Model Inference Availability: 99% (7-day window)
- Model Inference Latency P99: 500ms (7-day window)
- Model Accuracy Maintenance: 95% of baseline (30-day window)

**Recording Rules:**
- `sentinel:inference:availability:ratio_7d` - 7-day inference availability
- `sentinel:inference:latency:p99_7d` - 7-day P99 inference latency
- `sentinel:model:accuracy:current` - Current model accuracy
- `sentinel:model:drift_rate:7d` - 7-day drift detection rate

### 3. chronos-data-platform (Data Engineering)

**Business Metrics:**
- `airflow_dag_execution_duration_seconds` - DAG execution time
- `airflow_task_success_rate` - Task success rate by DAG
- `data_quality_check_failures` - Data quality check failures
- `data_quality_check_success_total` - Successful quality checks
- `data_pipeline_latency_seconds` - End-to-end pipeline latency
- `dbt_model_execution_time_seconds` - dbt model execution time
- `records_processed_total` - Records processed by pipeline
- `data_freshness_lag_seconds` - Data freshness lag
- `data_volume_bytes` - Data volume processed
- `data_schema_changes_detected` - Schema change detection

**SLOs:**
- Pipeline Success Rate: 99% (7-day window)
- Pipeline Latency P95: 1 hour (7-day window)
- Data Quality Check Success Rate: 99% (7-day window)

**Recording Rules:**
- `chronos:pipeline:success_rate:7d` - 7-day pipeline success rate
- `chronos:pipeline:latency:p95_7d` - 7-day P95 pipeline latency
- `chronos:data_quality:success_rate:7d` - 7-day data quality success rate
- `chronos:records:processing_rate:1h` - Hourly record processing rate

### 4. titan-microservices-mesh (Distributed Systems)

**Business Metrics:**
- `service_request_duration_seconds` - Service request latency
- `service_error_rate` - Service error rate by type
- `circuit_breaker_state` - Circuit breaker state (0=closed, 1=open, 2=half-open)
- `event_processing_latency_seconds` - Event processing time
- `events_processed_total` - Total events processed
- `event_processing_failures_total` - Event processing failures
- `distributed_trace_span_count` - Spans per distributed trace
- `service_dependency_health` - Dependency health status
- `service_request_queue_depth` - Request queue depth
- `service_retry_attempts` - Retry attempt count

**SLOs:**
- Service Availability: 99.9% (30-day window)
- Service Latency P99: 100ms (7-day window)
- Event Processing Success Rate: 99% (7-day window)
- Circuit Breaker Availability: 99.9% (7-day window)

**Recording Rules:**
- `titan:service:availability:ratio_30d` - 30-day service availability
- `titan:service:latency:p99_7d` - 7-day P99 service latency
- `titan:events:success_rate:7d` - 7-day event processing success rate
- `titan:circuit_breaker:closed_ratio:7d` - 7-day circuit breaker closed ratio

### 5. obsidian-devsecops-platform (Security)

**Business Metrics:**
- `security_scan_critical_findings` - Critical security findings
- `security_scan_high_findings` - High severity findings
- `security_scan_medium_findings` - Medium severity findings
- `security_scan_low_findings` - Low severity findings
- `security_scan_findings_by_category` - Findings by category
- `security_scan_remediation_status` - Remediation status
- `security_scan_execution_time_seconds` - Scan execution time
- `security_scan_failures_total` - Scan failure count
- `policy_violations_total` - Policy violations detected
- `policy_evaluations_total` - Total policy evaluations
- `security_finding_remediation_duration_seconds` - Remediation time
- `vulnerability_age_days` - Age of unresolved vulnerabilities

**SLOs:**
- Security Scan Execution Success: 99% (7-day window)
- Critical Findings Remediation Time: 24 hours (30-day window)
- Zero Critical Findings: 0 (30-day window)
- Policy Compliance Rate: 99% (30-day window)

**Recording Rules:**
- `obsidian:scan:success_rate:7d` - 7-day scan success rate
- `obsidian:findings:critical:current` - Current critical findings
- `obsidian:policy:compliance_rate:30d` - 30-day policy compliance
- `obsidian:findings:trend:7d` - 7-day findings trend

### 6. aurora-fullstack-saas (Full-Stack Application)

**Business Metrics:**
- `user_registration_total` - User registrations by source
- `user_registration_failures_total` - Failed registrations
- `user_login_total` - User logins by method
- `user_session_duration_seconds` - Session duration by role
- `api_endpoint_latency_seconds` - API endpoint latency
- `websocket_message_latency_seconds` - WebSocket message latency
- `active_websocket_connections` - Active WebSocket connections
- `database_query_duration_seconds` - Database query time
- `user_activity_events` - User activity by event type
- `api_authentication_failures` - Authentication failures
- `api_authorization_failures` - Authorization failures
- `cache_hit_rate` - Cache hit rate

**SLOs:**
- API Availability: 99.9% (30-day window)
- API Latency P99: 100ms (7-day window)
- WebSocket Connection Stability: 99% (7-day window)
- Database Query Latency P95: 50ms (7-day window)
- User Registration Success Rate: 99% (7-day window)

**Recording Rules:**
- `aurora:api:availability:ratio_30d` - 30-day API availability
- `aurora:api:latency:p99_7d` - 7-day P99 API latency
- `aurora:websocket:stability:7d` - 7-day WebSocket stability
- `aurora:database:latency:p95_7d` - 7-day P95 database latency
- `aurora:registration:success_rate:7d` - 7-day registration success rate

## SLO Tracking

### SLO Metrics

All meta-repositories expose these standardized SLO metrics:

- `slo_availability` - Service availability (0-1)
- `slo_latency_p99` - P99 latency in seconds
- `slo_error_rate` - Error rate (0-1)
- `slo_compliance` - SLO compliance percentage (0-100)
- `slo_budget_remaining` - Remaining error budget (0-1)

### Using the SLOTracker Class

```python
from metrics.custom_metrics import SLOTracker

# Initialize SLO tracker
slo_tracker = SLOTracker(
    service_name='my-service',
    slo_definitions={
        'availability': {'target': 0.999, 'window': 30},
        'latency_p99': {'target': 0.1, 'window': 7},
        'error_rate': {'target': 0.001, 'window': 7}
    }
)

# Record availability
slo_tracker.record_availability(available=True)

# Record latency
slo_tracker.record_latency(latency_seconds=0.085)

# Calculate compliance
compliance = slo_tracker.calculate_compliance('availability', actual_value=0.9995)
print(f"Availability compliance: {compliance}%")

# Calculate error budget
budget = slo_tracker.calculate_error_budget('error_rate', actual_value=0.0005)
print(f"Remaining error budget: {budget}")
```

## Alerting

### Alert Severity Levels

- **Critical**: Immediate action required (SLO violation, critical findings)
- **Warning**: Attention needed (approaching thresholds, degraded performance)

### Key Alerts

**Cross-Meta-Repo:**
- `SLOErrorBudgetExhausted` - Error budget completely consumed
- `SLOErrorBudgetBurningFast` - Error budget burning at >10x normal rate
- `SLOComplianceLow` - Overall SLO compliance <95%
- `MultipleSLOViolations` - >3 SLO violations in 24 hours

**Per Meta-Repo:**
- Availability SLO violations
- Latency SLO violations
- Business-specific thresholds (e.g., critical security findings, model drift)

### Alert Configuration

Alerts are defined in `prometheus/alerting-rules.yml` and evaluated every 1 minute.

## Usage Examples

### Recording Cost Metrics (nebula-cloud-platform)

```python
from metrics.custom_metrics import record_cost_metrics

record_cost_metrics(
    cloud_run_requests=150000,
    firestore_reads=25000,
    firestore_writes=10000,
    firestore_storage_bytes=536870912,  # 512MB
    cloud_storage_bytes=2684354560,  # 2.5GB
    service='my-service',
    region='us-central1'
)
```

### Recording Model Metrics (sentinel-ai-engine)

```python
from metrics.custom_metrics import record_model_metrics

record_model_metrics(
    model_name='yolov8-custom',
    accuracy=0.96,
    inference_latency_seconds=0.085,
    model_version='v1.2.0'
)
```

### Recording Pipeline Metrics (chronos-data-platform)

```python
from metrics.custom_metrics import record_pipeline_metrics

record_pipeline_metrics(
    pipeline_name='daily-etl',
    execution_duration_seconds=1850,
    records_processed=1000000,
    success=True
)
```

### Recording Service Metrics (titan-microservices-mesh)

```python
from metrics.custom_metrics import record_service_metrics

record_service_metrics(
    service='order-service',
    endpoint='/api/orders',
    method='POST',
    latency_seconds=0.045,
    status_code=201
)
```

### Recording Security Metrics (obsidian-devsecops-platform)

```python
from metrics.custom_metrics import record_security_metrics

record_security_metrics(
    scanner='checkov',
    resource_type='terraform',
    critical=0,
    high=2,
    medium=5,
    low=10
)
```

## Grafana Dashboards

Pre-built Grafana dashboards are available in `grafana/provisioning/dashboards/`:

1. **business-metrics.json** - Business-specific metrics per meta-repo
2. **slo-tracking.json** - SLO compliance and error budget tracking

Access Grafana at: http://localhost:3000 (admin/admin)

## Prometheus Configuration

### Scrape Configuration

Prometheus scrapes metrics from all meta-repositories every 15 seconds:

```yaml
scrape_configs:
  - job_name: 'nebula-cloud-platform'
    static_configs:
      - targets: ['localhost:8001']
  
  - job_name: 'sentinel-ai-engine'
    static_configs:
      - targets: ['localhost:8002']
  
  # ... (other meta-repos)
```

### Recording Rules

Recording rules pre-compute SLO metrics every 30 seconds for efficient querying:

```yaml
- record: nebula:api:availability:ratio_30d
  expr: |
    sum(rate(http_requests_total{status=~"2.."}[30d]))
    /
    sum(rate(http_requests_total[30d]))
```

### Alerting Rules

Alerting rules evaluate every 1 minute and trigger alerts on violations:

```yaml
- alert: NebulaAPIAvailabilitySLOViolation
  expr: nebula:api:availability:ratio_30d < 0.999
  for: 5m
  labels:
    severity: critical
```

## Integration with Meta-Repositories

Each meta-repository should:

1. **Import the metrics module:**
   ```python
   from shared_infrastructure.metrics.custom_metrics import (
       model_inference_latency,
       model_predictions_total,
       SLOTracker
   )
   ```

2. **Expose /metrics endpoint:**
   ```python
   from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
   from fastapi import Response
   
   @app.get("/metrics")
   def metrics():
       return Response(
           content=generate_latest(),
           media_type=CONTENT_TYPE_LATEST
       )
   ```

3. **Record metrics in application code:**
   ```python
   # Record inference latency
   start_time = time.time()
   prediction = model.predict(input_data)
   latency = time.time() - start_time
   
   model_inference_latency.labels(
       model_name='yolov8',
       model_version='v1.0'
   ).observe(latency)
   
   model_predictions_total.labels(
       model_name='yolov8',
       model_version='v1.0',
       prediction_type='object_detection'
   ).inc()
   ```

4. **Initialize SLO tracker:**
   ```python
   slo_tracker = SLOTracker(
       service_name='sentinel-inference',
       slo_definitions={
           'availability': {'target': 0.99, 'window': 7},
           'latency_p99': {'target': 0.5, 'window': 7}
       }
   )
   ```

## Testing

### Local Testing

1. Start the monitoring stack:
   ```bash
   cd shared-infrastructure
   docker-compose up -d prometheus grafana
   ```

2. Verify Prometheus is scraping:
   - Open http://localhost:9090
   - Go to Status → Targets
   - Verify all targets are "UP"

3. Check recording rules:
   - Go to Status → Rules
   - Verify all recording rules are evaluating

4. Check alerting rules:
   - Go to Alerts
   - Verify rules are loaded (should be green/inactive)

5. Access Grafana:
   - Open http://localhost:3000
   - Login: admin/admin
   - Navigate to Dashboards → Browse
   - Open "Business Metrics" or "SLO Tracking"

### Simulating Metrics

```python
# Simulate metrics for testing
from metrics.custom_metrics import *
import random
import time

while True:
    # Simulate API requests
    latency = random.uniform(0.01, 0.2)
    api_endpoint_latency.labels(
        endpoint='/api/test',
        method='GET'
    ).observe(latency)
    
    # Simulate model predictions
    model_predictions_total.labels(
        model_name='test-model',
        model_version='v1.0',
        prediction_type='classification'
    ).inc()
    
    time.sleep(1)
```

## Troubleshooting

### Metrics Not Appearing in Prometheus

1. Check if service is exposing /metrics endpoint:
   ```bash
   curl http://localhost:8001/metrics
   ```

2. Check Prometheus scrape configuration:
   ```bash
   docker logs shared-prometheus
   ```

3. Verify target is UP in Prometheus UI:
   - http://localhost:9090/targets

### Recording Rules Not Evaluating

1. Check Prometheus logs:
   ```bash
   docker logs shared-prometheus
   ```

2. Verify rule syntax:
   ```bash
   promtool check rules prometheus/recording-rules.yml
   ```

3. Check rule evaluation in Prometheus UI:
   - http://localhost:9090/rules

### Alerts Not Firing

1. Verify alerting rules are loaded:
   - http://localhost:9090/alerts

2. Check alert expression manually:
   - Go to Prometheus → Graph
   - Enter alert expression
   - Verify it returns expected results

3. Check alert "for" duration:
   - Alerts only fire after condition is true for specified duration

## Best Practices

1. **Use labels consistently** - Maintain consistent label names across metrics
2. **Avoid high cardinality** - Don't use user IDs or timestamps as labels
3. **Use histograms for latencies** - Better than gauges for percentile calculations
4. **Pre-compute with recording rules** - Reduce query load on Prometheus
5. **Set appropriate SLO targets** - Based on business requirements, not arbitrary numbers
6. **Monitor error budgets** - Track how fast you're consuming error budget
7. **Test alerts** - Regularly test that alerts fire correctly
8. **Document custom metrics** - Add clear descriptions and usage examples

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [SLO Implementation Guide](https://sre.google/workbook/implementing-slos/)
- [Grafana Documentation](https://grafana.com/docs/)
- [OpenMetrics Specification](https://openmetrics.io/)

## Support

For questions or issues with metrics and SLO tracking:
1. Check this README
2. Review Prometheus logs: `docker logs shared-prometheus`
3. Review Grafana logs: `docker logs shared-grafana`
4. Check the design document: `.kiro/specs/meta-repository-consolidation/design.md`
