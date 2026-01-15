"""
Monitoring and Metrics
"""

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

# Metrics
request_count = Counter('aiza_requests_total', 'Total requests')
request_duration = Histogram('aiza_request_duration_seconds', 'Request duration')
error_count = Counter('aiza_errors_total', 'Total errors')


def setup_monitoring():
    """Setup monitoring"""
    pass


def get_metrics():
    """Get Prometheus metrics"""
    return generate_latest()
