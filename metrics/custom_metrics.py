"""
Custom Metrics Module for Meta-Repository Consolidation

This module provides business-specific metrics and SLO tracking for all meta-repos.
Metrics are exposed in Prometheus format for collection by Prometheus.
"""

from prometheus_client import Counter, Gauge, Histogram, Summary
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import time

# ============================================================================
# Business Metrics - nebula-cloud-platform
# ============================================================================

# Cost tracking metrics
gcp_usage_cloud_run_requests = Gauge(
    'gcp_usage_cloud_run_requests',
    'Total Cloud Run requests used (out of 2M free tier limit)',
    ['service', 'region']
)

gcp_usage_firestore_reads = Gauge(
    'gcp_usage_firestore_reads',
    'Total Firestore read operations (out of 50k/day free tier limit)',
    ['database', 'collection']
)

gcp_usage_firestore_writes = Gauge(
    'gcp_usage_firestore_writes',
    'Total Firestore write operations (out of 20k/day free tier limit)',
    ['database', 'collection']
)

gcp_usage_firestore_storage = Gauge(
    'gcp_usage_firestore_storage',
    'Firestore storage used in bytes (out of 1GB free tier limit)',
    ['database']
)

gcp_usage_cloud_storage = Gauge(
    'gcp_usage_cloud_storage',
    'Cloud Storage used in bytes (out of 5GB free tier limit)',
    ['bucket']
)

gcp_cost_by_service = Gauge(
    'gcp_cost_by_service',
    'Estimated monthly cost by service (in USD)',
    ['service']
)

cost_forecast_accuracy = Gauge(
    'cost_forecast_accuracy',
    'Accuracy of cost forecasting model (0-1)',
    ['forecast_period']
)

# Infrastructure resource utilization
infrastructure_cpu_utilization = Gauge(
    'infrastructure_cpu_utilization',
    'CPU utilization percentage for infrastructure resources',
    ['resource_type', 'resource_name']
)

infrastructure_memory_utilization = Gauge(
    'infrastructure_memory_utilization',
    'Memory utilization percentage for infrastructure resources',
    ['resource_type', 'resource_name']
)

infrastructure_deployment_duration = Histogram(
    'infrastructure_deployment_duration_seconds',
    'Time taken to deploy infrastructure resources',
    ['resource_type'],
    buckets=(30, 60, 120, 300, 600, 1800)
)

infrastructure_drift_detected = Gauge(
    'infrastructure_drift_detected',
    'Whether infrastructure drift has been detected (0=no, 1=yes)',
    ['resource_type', 'resource_name']
)

# ============================================================================
# Business Metrics - sentinel-ai-engine
# ============================================================================

model_training_duration = Histogram(
    'model_training_duration_seconds',
    'Time taken to train a model',
    ['model_name', 'framework'],
    buckets=(60, 300, 600, 1800, 3600, 7200)
)

model_inference_latency = Histogram(
    'model_inference_latency_seconds',
    'Time taken for model inference',
    ['model_name', 'model_version'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0)
)

model_accuracy = Gauge(
    'model_accuracy',
    'Model accuracy metric',
    ['model_name', 'model_version', 'metric_type']
)

model_predictions_total = Counter(
    'model_predictions_total',
    'Total number of predictions made',
    ['model_name', 'model_version', 'prediction_type']
)

model_drift_detected = Gauge(
    'model_drift_detected',
    'Whether model drift has been detected (0=no, 1=yes)',
    ['model_name', 'model_version']
)

model_training_failures_total = Counter(
    'model_training_failures_total',
    'Total number of model training failures',
    ['model_name', 'failure_reason']
)

model_data_quality_score = Gauge(
    'model_data_quality_score',
    'Data quality score for training data (0-1)',
    ['model_name', 'dataset_name']
)

model_feature_importance = Gauge(
    'model_feature_importance',
    'Feature importance scores',
    ['model_name', 'feature_name']
)

model_prediction_confidence = Histogram(
    'model_prediction_confidence',
    'Confidence scores of model predictions',
    ['model_name', 'model_version'],
    buckets=(0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99)
)

# ============================================================================
# Business Metrics - chronos-data-platform
# ============================================================================

airflow_dag_execution_duration = Histogram(
    'airflow_dag_execution_duration_seconds',
    'Time taken to execute an Airflow DAG',
    ['dag_id'],
    buckets=(60, 300, 600, 1800, 3600, 7200, 14400)
)

airflow_task_success_rate = Gauge(
    'airflow_task_success_rate',
    'Success rate of Airflow tasks (0-1)',
    ['dag_id', 'task_id']
)

data_quality_check_failures = Counter(
    'data_quality_check_failures',
    'Number of data quality check failures',
    ['check_name', 'data_source']
)

data_quality_check_success_total = Counter(
    'data_quality_check_success_total',
    'Number of successful data quality checks',
    ['check_name', 'data_source']
)

data_pipeline_latency = Histogram(
    'data_pipeline_latency_seconds',
    'End-to-end data pipeline latency',
    ['pipeline_name'],
    buckets=(60, 300, 600, 1800, 3600, 7200)
)

dbt_model_execution_time = Histogram(
    'dbt_model_execution_time_seconds',
    'Time taken to execute a dbt model',
    ['model_name', 'model_type'],
    buckets=(10, 30, 60, 300, 600)
)

records_processed_total = Counter(
    'records_processed_total',
    'Total number of records processed',
    ['pipeline_name', 'stage']
)

data_freshness_lag = Gauge(
    'data_freshness_lag_seconds',
    'Time lag between data generation and availability',
    ['data_source', 'table_name']
)

data_volume_bytes = Gauge(
    'data_volume_bytes',
    'Volume of data processed in bytes',
    ['pipeline_name', 'stage']
)

data_schema_changes_detected = Counter(
    'data_schema_changes_detected',
    'Number of schema changes detected',
    ['data_source', 'table_name']
)

# ============================================================================
# Business Metrics - titan-microservices-mesh
# ============================================================================

service_request_duration = Histogram(
    'service_request_duration_seconds',
    'Request duration for microservices',
    ['service', 'endpoint', 'method'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0, 5.0)
)

service_error_rate = Gauge(
    'service_error_rate',
    'Error rate for each service (0-1)',
    ['service', 'error_type']
)

circuit_breaker_state = Gauge(
    'circuit_breaker_state',
    'Circuit breaker state (0=closed, 1=open, 2=half-open)',
    ['service', 'dependency']
)

event_processing_latency = Histogram(
    'event_processing_latency_seconds',
    'Time taken to process an event',
    ['event_type', 'consumer_service'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0)
)

events_processed_total = Counter(
    'events_processed_total',
    'Total number of events processed',
    ['event_type', 'consumer_service']
)

event_processing_failures_total = Counter(
    'event_processing_failures_total',
    'Total number of event processing failures',
    ['event_type', 'consumer_service', 'failure_reason']
)

distributed_trace_span_count = Gauge(
    'distributed_trace_span_count',
    'Number of spans in a distributed trace',
    ['trace_id', 'service']
)

service_dependency_health = Gauge(
    'service_dependency_health',
    'Health status of service dependencies (0=unhealthy, 1=healthy)',
    ['service', 'dependency']
)

service_request_queue_depth = Gauge(
    'service_request_queue_depth',
    'Number of requests in service queue',
    ['service']
)

service_retry_attempts = Counter(
    'service_retry_attempts',
    'Number of retry attempts for failed requests',
    ['service', 'endpoint']
)

# ============================================================================
# Business Metrics - obsidian-devsecops-platform
# ============================================================================

security_scan_critical_findings = Gauge(
    'security_scan_critical_findings',
    'Number of critical security findings',
    ['scanner', 'resource_type']
)

security_scan_high_findings = Gauge(
    'security_scan_high_findings',
    'Number of high severity security findings',
    ['scanner', 'resource_type']
)

security_scan_medium_findings = Gauge(
    'security_scan_medium_findings',
    'Number of medium severity security findings',
    ['scanner', 'resource_type']
)

security_scan_low_findings = Gauge(
    'security_scan_low_findings',
    'Number of low severity security findings',
    ['scanner', 'resource_type']
)

security_scan_findings_by_category = Gauge(
    'security_scan_findings_by_category',
    'Security findings grouped by category',
    ['category', 'severity']
)

security_scan_remediation_status = Gauge(
    'security_scan_remediation_status',
    'Number of findings by remediation status',
    ['status']
)

security_scan_execution_time = Histogram(
    'security_scan_execution_time_seconds',
    'Time taken to execute security scans',
    ['scanner', 'resource_type'],
    buckets=(10, 30, 60, 300, 600, 1800)
)

security_scan_failures_total = Counter(
    'security_scan_failures_total',
    'Total number of security scan failures',
    ['scanner', 'failure_reason']
)

security_scan_trend = Gauge(
    'security_scan_trend',
    'Trend of security findings over time',
    ['severity']
)

policy_violations_total = Counter(
    'policy_violations_total',
    'Total number of policy violations detected',
    ['policy_name', 'resource_type']
)

policy_evaluations_total = Counter(
    'policy_evaluations_total',
    'Total number of policy evaluations',
    ['policy_name', 'resource_type']
)

security_finding_remediation_duration = Histogram(
    'security_finding_remediation_duration_seconds',
    'Time taken to remediate security findings',
    ['severity', 'category'],
    buckets=(3600, 7200, 14400, 43200, 86400, 172800)  # 1h to 2 days
)

vulnerability_age_days = Gauge(
    'vulnerability_age_days',
    'Age of unresolved vulnerabilities in days',
    ['vulnerability_id', 'severity']
)

# ============================================================================
# Business Metrics - aurora-fullstack-saas
# ============================================================================

user_registration_total = Counter(
    'user_registration_total',
    'Total number of user registrations',
    ['registration_source']
)

user_registration_failures_total = Counter(
    'user_registration_failures_total',
    'Total number of failed user registrations',
    ['failure_reason']
)

user_login_total = Counter(
    'user_login_total',
    'Total number of user logins',
    ['login_method']
)

user_session_duration = Histogram(
    'user_session_duration_seconds',
    'User session duration',
    ['user_role'],
    buckets=(60, 300, 600, 1800, 3600, 7200, 14400)
)

api_endpoint_latency = Histogram(
    'api_endpoint_latency_seconds',
    'API endpoint response latency',
    ['endpoint', 'method'],
    buckets=(0.01, 0.05, 0.1, 0.5, 1.0)
)

websocket_message_latency = Histogram(
    'websocket_message_latency_seconds',
    'WebSocket message delivery latency',
    ['message_type'],
    buckets=(0.001, 0.01, 0.05, 0.1, 0.5)
)

active_websocket_connections = Gauge(
    'active_websocket_connections',
    'Number of active WebSocket connections',
    ['connection_type']
)

database_query_duration = Histogram(
    'database_query_duration_seconds',
    'Database query execution time',
    ['query_type', 'table'],
    buckets=(0.001, 0.01, 0.05, 0.1, 0.5, 1.0)
)

user_activity_events = Counter(
    'user_activity_events',
    'User activity events by type',
    ['event_type', 'user_role']
)

api_authentication_failures = Counter(
    'api_authentication_failures',
    'Number of API authentication failures',
    ['failure_reason']
)

api_authorization_failures = Counter(
    'api_authorization_failures',
    'Number of API authorization failures',
    ['endpoint', 'user_role']
)

cache_hit_rate = Gauge(
    'cache_hit_rate',
    'Cache hit rate (0-1)',
    ['cache_type']
)

# ============================================================================
# SLO Metrics (Cross-Meta-Repo)
# ============================================================================

slo_availability = Gauge(
    'slo_availability',
    'Service availability SLO (0-1)',
    ['service', 'slo_name']
)

slo_latency_p99 = Gauge(
    'slo_latency_p99',
    'P99 latency SLO in seconds',
    ['service', 'slo_name']
)

slo_error_rate = Gauge(
    'slo_error_rate',
    'Error rate SLO (0-1)',
    ['service', 'slo_name']
)

slo_compliance = Gauge(
    'slo_compliance',
    'SLO compliance percentage (0-100)',
    ['service', 'slo_name']
)

slo_budget_remaining = Gauge(
    'slo_budget_remaining',
    'Remaining error budget for SLO (0-1)',
    ['service', 'slo_name']
)

# ============================================================================
# Helper Functions for SLO Tracking
# ============================================================================

class SLOTracker:
    """Track Service Level Objectives across meta-repos"""
    
    def __init__(self, service_name: str, slo_definitions: Dict[str, Dict]):
        """
        Initialize SLO tracker
        
        Args:
            service_name: Name of the service
            slo_definitions: Dict of SLO definitions with targets
                Example: {
                    'availability': {'target': 0.999, 'window': 30},  # 30 days
                    'latency_p99': {'target': 0.1, 'window': 7},  # 7 days
                    'error_rate': {'target': 0.001, 'window': 7}
                }
        """
        self.service_name = service_name
        self.slo_definitions = slo_definitions
        self.metrics_history: Dict[str, List[tuple]] = {}
    
    def record_availability(self, available: bool, slo_name: str = 'availability'):
        """Record service availability"""
        slo_availability.labels(
            service=self.service_name,
            slo_name=slo_name
        ).set(1.0 if available else 0.0)
    
    def record_latency(self, latency_seconds: float, slo_name: str = 'latency_p99'):
        """Record service latency"""
        slo_latency_p99.labels(
            service=self.service_name,
            slo_name=slo_name
        ).set(latency_seconds)
    
    def record_error_rate(self, error_rate: float, slo_name: str = 'error_rate'):
        """Record service error rate"""
        slo_error_rate.labels(
            service=self.service_name,
            slo_name=slo_name
        ).set(error_rate)
    
    def calculate_compliance(self, slo_name: str, actual_value: float) -> float:
        """
        Calculate SLO compliance percentage
        
        Returns:
            Compliance percentage (0-100)
        """
        if slo_name not in self.slo_definitions:
            return 0.0
        
        target = self.slo_definitions[slo_name]['target']
        
        # For availability and error_rate, higher is better
        if slo_name in ['availability', 'error_rate']:
            compliance = min(100.0, (actual_value / target) * 100)
        else:
            # For latency, lower is better
            compliance = min(100.0, (target / actual_value) * 100)
        
        slo_compliance.labels(
            service=self.service_name,
            slo_name=slo_name
        ).set(compliance)
        
        return compliance
    
    def calculate_error_budget(self, slo_name: str, actual_value: float) -> float:
        """
        Calculate remaining error budget
        
        Returns:
            Remaining budget as fraction (0-1)
        """
        if slo_name not in self.slo_definitions:
            return 0.0
        
        target = self.slo_definitions[slo_name]['target']
        
        # Error budget = target - actual
        if slo_name == 'error_rate':
            budget = max(0.0, target - actual_value)
        else:
            budget = max(0.0, actual_value - target)
        
        slo_budget_remaining.labels(
            service=self.service_name,
            slo_name=slo_name
        ).set(budget)
        
        return budget


# ============================================================================
# Helper Functions for Metrics Recording
# ============================================================================

def record_cost_metrics(
    cloud_run_requests: int,
    firestore_reads: int,
    firestore_writes: int,
    firestore_storage_bytes: int,
    cloud_storage_bytes: int,
    service: str = 'default',
    region: str = 'us-central1'
):
    """Record GCP usage metrics"""
    gcp_usage_cloud_run_requests.labels(service=service, region=region).set(cloud_run_requests)
    gcp_usage_firestore_reads.labels(database=service, collection='all').set(firestore_reads)
    gcp_usage_firestore_writes.labels(database=service, collection='all').set(firestore_writes)
    gcp_usage_firestore_storage.labels(database=service).set(firestore_storage_bytes)
    gcp_usage_cloud_storage.labels(bucket=service).set(cloud_storage_bytes)


def record_model_metrics(
    model_name: str,
    accuracy: float,
    inference_latency_seconds: float,
    model_version: str = 'latest'
):
    """Record ML model metrics"""
    model_accuracy.labels(
        model_name=model_name,
        model_version=model_version,
        metric_type='accuracy'
    ).set(accuracy)
    
    model_inference_latency.labels(
        model_name=model_name,
        model_version=model_version
    ).observe(inference_latency_seconds)


def record_pipeline_metrics(
    pipeline_name: str,
    execution_duration_seconds: float,
    records_processed: int,
    success: bool
):
    """Record data pipeline metrics"""
    data_pipeline_latency.labels(pipeline_name=pipeline_name).observe(execution_duration_seconds)
    records_processed_total.labels(pipeline_name=pipeline_name, stage='completed').inc(records_processed)
    
    if not success:
        data_quality_check_failures.labels(
            check_name=pipeline_name,
            data_source='pipeline'
        ).inc()


def record_service_metrics(
    service: str,
    endpoint: str,
    method: str,
    latency_seconds: float,
    status_code: int
):
    """Record microservice metrics"""
    service_request_duration.labels(
        service=service,
        endpoint=endpoint,
        method=method
    ).observe(latency_seconds)
    
    if status_code >= 500:
        service_error_rate.labels(
            service=service,
            error_type=f'http_{status_code}'
        ).inc()


def record_security_metrics(
    scanner: str,
    resource_type: str,
    critical: int,
    high: int,
    medium: int,
    low: int
):
    """Record security scan metrics"""
    security_scan_critical_findings.labels(
        scanner=scanner,
        resource_type=resource_type
    ).set(critical)
    
    security_scan_high_findings.labels(
        scanner=scanner,
        resource_type=resource_type
    ).set(high)
    
    security_scan_medium_findings.labels(
        scanner=scanner,
        resource_type=resource_type
    ).set(medium)
    
    security_scan_low_findings.labels(
        scanner=scanner,
        resource_type=resource_type
    ).set(low)
