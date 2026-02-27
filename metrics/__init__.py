"""
Metrics module for meta-repository consolidation

Provides business-specific metrics and SLO tracking for all meta-repos.
"""

from .custom_metrics import (
    # Cost metrics
    gcp_usage_cloud_run_requests,
    gcp_usage_firestore_reads,
    gcp_usage_firestore_writes,
    gcp_usage_firestore_storage,
    gcp_usage_cloud_storage,
    gcp_cost_by_service,
    cost_forecast_accuracy,
    
    # ML metrics
    model_training_duration,
    model_inference_latency,
    model_accuracy,
    model_predictions_total,
    model_drift_detected,
    
    # Data pipeline metrics
    airflow_dag_execution_duration,
    airflow_task_success_rate,
    data_quality_check_failures,
    data_pipeline_latency,
    dbt_model_execution_time,
    records_processed_total,
    
    # Microservices metrics
    service_request_duration,
    service_error_rate,
    circuit_breaker_state,
    event_processing_latency,
    events_processed_total,
    distributed_trace_span_count,
    
    # Security metrics
    security_scan_critical_findings,
    security_scan_high_findings,
    security_scan_medium_findings,
    security_scan_low_findings,
    security_scan_findings_by_category,
    security_scan_remediation_status,
    security_scan_execution_time,
    security_scan_trend,
    policy_violations_total,
    
    # SaaS metrics
    user_registration_total,
    user_login_total,
    user_session_duration,
    api_endpoint_latency,
    websocket_message_latency,
    active_websocket_connections,
    database_query_duration,
    
    # SLO metrics
    slo_availability,
    slo_latency_p99,
    slo_error_rate,
    slo_compliance,
    slo_budget_remaining,
    
    # Helper classes and functions
    SLOTracker,
    record_cost_metrics,
    record_model_metrics,
    record_pipeline_metrics,
    record_service_metrics,
    record_security_metrics,
)

__all__ = [
    # Cost metrics
    'gcp_usage_cloud_run_requests',
    'gcp_usage_firestore_reads',
    'gcp_usage_firestore_writes',
    'gcp_usage_firestore_storage',
    'gcp_usage_cloud_storage',
    'gcp_cost_by_service',
    'cost_forecast_accuracy',
    
    # ML metrics
    'model_training_duration',
    'model_inference_latency',
    'model_accuracy',
    'model_predictions_total',
    'model_drift_detected',
    
    # Data pipeline metrics
    'airflow_dag_execution_duration',
    'airflow_task_success_rate',
    'data_quality_check_failures',
    'data_pipeline_latency',
    'dbt_model_execution_time',
    'records_processed_total',
    
    # Microservices metrics
    'service_request_duration',
    'service_error_rate',
    'circuit_breaker_state',
    'event_processing_latency',
    'events_processed_total',
    'distributed_trace_span_count',
    
    # Security metrics
    'security_scan_critical_findings',
    'security_scan_high_findings',
    'security_scan_medium_findings',
    'security_scan_low_findings',
    'security_scan_findings_by_category',
    'security_scan_remediation_status',
    'security_scan_execution_time',
    'security_scan_trend',
    'policy_violations_total',
    
    # SaaS metrics
    'user_registration_total',
    'user_login_total',
    'user_session_duration',
    'api_endpoint_latency',
    'websocket_message_latency',
    'active_websocket_connections',
    'database_query_duration',
    
    # SLO metrics
    'slo_availability',
    'slo_latency_p99',
    'slo_error_rate',
    'slo_compliance',
    'slo_budget_remaining',
    
    # Helper classes and functions
    'SLOTracker',
    'record_cost_metrics',
    'record_model_metrics',
    'record_pipeline_metrics',
    'record_service_metrics',
    'record_security_metrics',
]
