"""
Example Integration: Custom Metrics and SLO Tracking

This file demonstrates how to integrate custom metrics and SLO tracking
into a FastAPI application for any meta-repository.

Usage:
    1. Copy relevant sections to your application
    2. Adjust metric names and labels for your use case
    3. Initialize SLO tracker with your targets
    4. Add metrics recording to your business logic
"""

from fastapi import FastAPI, Request, Response, HTTPException
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time
from typing import Optional
import logging

# Import custom metrics (adjust based on your meta-repo)
from custom_metrics import (
    # Common metrics
    api_endpoint_latency,
    
    # Meta-repo specific metrics (uncomment as needed)
    # nebula-cloud-platform
    # gcp_usage_cloud_run_requests,
    # cost_forecast_accuracy,
    
    # sentinel-ai-engine
    # model_inference_latency,
    # model_predictions_total,
    # model_accuracy,
    
    # chronos-data-platform
    # data_pipeline_latency,
    # records_processed_total,
    # data_quality_check_failures,
    
    # titan-microservices-mesh
    # service_request_duration,
    # circuit_breaker_state,
    # events_processed_total,
    
    # obsidian-devsecops-platform
    # security_scan_critical_findings,
    # policy_violations_total,
    
    # aurora-fullstack-saas
    # user_registration_total,
    # active_websocket_connections,
    # database_query_duration,
    
    # SLO tracking
    SLOTracker
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Meta-Repository Service",
    description="Example service with custom metrics and SLO tracking",
    version="1.0.0"
)

# ============================================================================
# SLO Tracker Initialization
# ============================================================================

# Initialize SLO tracker with your service's targets
slo_tracker = SLOTracker(
    service_name='example-service',
    slo_definitions={
        'availability': {
            'target': 0.999,  # 99.9% availability
            'window': 30      # 30-day window
        },
        'latency_p99': {
            'target': 0.1,    # 100ms P99 latency
            'window': 7       # 7-day window
        },
        'error_rate': {
            'target': 0.001,  # 0.1% error rate
            'window': 7       # 7-day window
        }
    }
)

# ============================================================================
# Middleware for Automatic Metrics Collection
# ============================================================================

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """
    Middleware to automatically collect metrics for all requests.
    
    Tracks:
    - Request latency
    - Availability (based on status code)
    - Error rate
    - SLO compliance
    """
    start_time = time.time()
    path = request.url.path
    method = request.method
    
    try:
        # Process request
        response = await call_next(request)
        
        # Calculate latency
        latency = time.time() - start_time
        
        # Record API endpoint latency
        api_endpoint_latency.labels(
            endpoint=path,
            method=method
        ).observe(latency)
        
        # Record availability (5xx = unavailable)
        available = response.status_code < 500
        slo_tracker.record_availability(available, slo_name='availability')
        
        # Record latency for SLO tracking
        slo_tracker.record_latency(latency, slo_name='latency_p99')
        
        # Calculate and record error rate
        if response.status_code >= 400:
            # In production, calculate actual error rate from metrics
            error_rate = 0.001  # Placeholder
            slo_tracker.record_error_rate(error_rate, slo_name='error_rate')
        
        # Log request
        logger.info(
            f"{method} {path} - {response.status_code} - {latency:.3f}s"
        )
        
        return response
        
    except Exception as e:
        # Record failure
        latency = time.time() - start_time
        slo_tracker.record_availability(False, slo_name='availability')
        
        logger.error(f"{method} {path} - ERROR - {latency:.3f}s - {str(e)}")
        raise

# ============================================================================
# Metrics Endpoint
# ============================================================================

@app.get("/metrics", include_in_schema=False)
def metrics():
    """
    Prometheus metrics endpoint.
    
    This endpoint exposes all metrics in Prometheus format for scraping.
    """
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

# ============================================================================
# Health Check Endpoints
# ============================================================================

@app.get("/health", tags=["Health"])
def health_check():
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "example-service"}

@app.get("/ready", tags=["Health"])
def readiness_check():
    """
    Readiness check endpoint.
    
    Returns 200 if service is ready to accept traffic,
    503 if not ready (e.g., dependencies unavailable).
    """
    # Check dependencies (database, cache, etc.)
    dependencies_ready = check_dependencies()
    
    if dependencies_ready:
        return {"status": "ready"}
    else:
        raise HTTPException(status_code=503, detail="Service not ready")

def check_dependencies() -> bool:
    """Check if all dependencies are available."""
    # Implement actual dependency checks
    # Example: database connection, cache connection, etc.
    return True

# ============================================================================
# Example API Endpoints with Metrics
# ============================================================================

@app.get("/api/data", tags=["API"])
def get_data():
    """
    Example endpoint that demonstrates metric recording.
    
    Metrics are automatically recorded by middleware, but you can
    add additional business-specific metrics here.
    """
    # Simulate data fetching
    time.sleep(0.05)  # Simulate 50ms latency
    
    # Business logic here
    data = {"message": "Hello, World!", "timestamp": time.time()}
    
    # Additional business-specific metrics can be recorded here
    # Example: record_custom_business_metric()
    
    return data

@app.post("/api/process", tags=["API"])
def process_data(data: dict):
    """
    Example endpoint that processes data and records custom metrics.
    """
    start_time = time.time()
    
    try:
        # Process data
        result = perform_processing(data)
        
        # Record processing duration
        processing_time = time.time() - start_time
        
        # Record business-specific metrics
        # Example for chronos-data-platform:
        # records_processed_total.labels(
        #     pipeline_name='api-processing',
        #     stage='transform'
        # ).inc(len(data.get('records', [])))
        
        return {"status": "success", "result": result}
        
    except Exception as e:
        # Record failure metrics
        logger.error(f"Processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Processing failed")

def perform_processing(data: dict) -> dict:
    """Simulate data processing."""
    time.sleep(0.1)  # Simulate processing time
    return {"processed": True, "count": len(data)}

# ============================================================================
# Example: Model Inference Endpoint (sentinel-ai-engine)
# ============================================================================

@app.post("/api/predict", tags=["ML"])
def predict(input_data: dict):
    """
    Example ML inference endpoint with metrics.
    
    Demonstrates how to record model-specific metrics.
    """
    start_time = time.time()
    
    try:
        # Perform inference
        prediction = run_model_inference(input_data)
        
        # Record inference latency
        latency = time.time() - start_time
        # model_inference_latency.labels(
        #     model_name='example-model',
        #     model_version='v1.0'
        # ).observe(latency)
        
        # Record prediction count
        # model_predictions_total.labels(
        #     model_name='example-model',
        #     model_version='v1.0',
        #     prediction_type='classification'
        # ).inc()
        
        return {
            "prediction": prediction,
            "confidence": 0.95,
            "latency_ms": latency * 1000
        }
        
    except Exception as e:
        logger.error(f"Inference failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Inference failed")

def run_model_inference(input_data: dict) -> str:
    """Simulate model inference."""
    time.sleep(0.08)  # Simulate inference time
    return "positive"

# ============================================================================
# Example: Data Pipeline Endpoint (chronos-data-platform)
# ============================================================================

@app.post("/api/pipeline/run", tags=["Data"])
def run_pipeline(pipeline_config: dict):
    """
    Example data pipeline endpoint with metrics.
    
    Demonstrates how to record pipeline-specific metrics.
    """
    start_time = time.time()
    pipeline_name = pipeline_config.get('name', 'default')
    
    try:
        # Run pipeline
        records_processed = execute_pipeline(pipeline_config)
        
        # Record pipeline duration
        duration = time.time() - start_time
        # data_pipeline_latency.labels(
        #     pipeline_name=pipeline_name
        # ).observe(duration)
        
        # Record records processed
        # records_processed_total.labels(
        #     pipeline_name=pipeline_name,
        #     stage='completed'
        # ).inc(records_processed)
        
        return {
            "status": "success",
            "records_processed": records_processed,
            "duration_seconds": duration
        }
        
    except Exception as e:
        # Record failure
        # data_quality_check_failures.labels(
        #     check_name=pipeline_name,
        #     data_source='api'
        # ).inc()
        
        logger.error(f"Pipeline failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Pipeline execution failed")

def execute_pipeline(config: dict) -> int:
    """Simulate pipeline execution."""
    time.sleep(0.5)  # Simulate pipeline execution
    return 1000  # Number of records processed

# ============================================================================
# Example: Security Scan Endpoint (obsidian-devsecops-platform)
# ============================================================================

@app.post("/api/security/scan", tags=["Security"])
def run_security_scan(scan_config: dict):
    """
    Example security scan endpoint with metrics.
    
    Demonstrates how to record security-specific metrics.
    """
    start_time = time.time()
    scanner = scan_config.get('scanner', 'default')
    resource_type = scan_config.get('resource_type', 'code')
    
    try:
        # Run security scan
        scan_results = perform_security_scan(scan_config)
        
        # Record scan duration
        duration = time.time() - start_time
        # security_scan_execution_time.labels(
        #     scanner=scanner,
        #     resource_type=resource_type
        # ).observe(duration)
        
        # Record findings
        # security_scan_critical_findings.labels(
        #     scanner=scanner,
        #     resource_type=resource_type
        # ).set(scan_results['critical'])
        
        return {
            "status": "success",
            "findings": scan_results,
            "duration_seconds": duration
        }
        
    except Exception as e:
        logger.error(f"Security scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Security scan failed")

def perform_security_scan(config: dict) -> dict:
    """Simulate security scan."""
    time.sleep(0.3)  # Simulate scan time
    return {
        "critical": 0,
        "high": 2,
        "medium": 5,
        "low": 10
    }

# ============================================================================
# SLO Status Endpoint
# ============================================================================

@app.get("/api/slo/status", tags=["SLO"])
def get_slo_status():
    """
    Get current SLO compliance status.
    
    Returns compliance percentages and error budget for all SLOs.
    """
    # In production, calculate actual values from Prometheus metrics
    # This is a simplified example
    
    return {
        "service": "example-service",
        "slos": {
            "availability": {
                "target": 0.999,
                "current": 0.9995,
                "compliance": 100.0,
                "error_budget_remaining": 0.0005
            },
            "latency_p99": {
                "target": 0.1,
                "current": 0.085,
                "compliance": 100.0,
                "error_budget_remaining": 0.015
            },
            "error_rate": {
                "target": 0.001,
                "current": 0.0005,
                "compliance": 100.0,
                "error_budget_remaining": 0.0005
            }
        }
    }

# ============================================================================
# Application Startup
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Application startup event.
    
    Initialize connections, load models, etc.
    """
    logger.info("Starting example service...")
    logger.info("SLO tracker initialized with targets:")
    for slo_name, slo_def in slo_tracker.slo_definitions.items():
        logger.info(f"  - {slo_name}: {slo_def['target']} ({slo_def['window']} days)")
    logger.info("Service ready to accept requests")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event.
    
    Clean up resources, close connections, etc.
    """
    logger.info("Shutting down example service...")

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
