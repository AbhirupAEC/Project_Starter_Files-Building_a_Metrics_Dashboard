import logging
import re
import requests
from flask import Flask, jsonify, render_template, request
from flask_opentracing import FlaskTracing
from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST, REGISTRY
import time


app = Flask(__name__)

metrics = PrometheusMetrics(app)
# static information as metric
metrics.info("app_info", "Application info", version="1.0.3")

# Custom metrics
REQUEST_COUNT = Counter('http_request_total', 'Total HTTP Requests', ['method', 'status', 'path'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['method', 'status', 'path'])
REQUEST_IN_PROGRESS = Gauge('http_requests_in_progress', 'HTTP Requests in progress', ['method', 'path'])
APP_UPTIME = Gauge('app_uptime_seconds', 'Application uptime in seconds')

# System metrics
CPU_USAGE = Gauge('process_cpu_usage', 'Current CPU usage in percent')
MEMORY_USAGE = Gauge('process_memory_usage_bytes', 'Current memory usage in bytes')
MEMORY_USAGE_MB = Gauge('app_memory_usage_mb', 'Memory usage in MB')

start_time = time.time()


logging.getLogger("").handlers = []
logging.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init_tracer(service):

    config = Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "logging": True,
            "reporter_batch_size": 1,
        },
        service_name=service,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(service_name_label=service),
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()

tracer = init_tracer("backend")
flask_tracer = FlaskTracing(tracer, True, app)


@app.route("/")
def homepage():
    return "Hello World"


@app.route("/api")
def my_api():
    answer = "something"
    return jsonify(repsonse=answer)

@app.route("/trace")
def trace():
    def remove_tags(text):
        tag = re.compile(r"<[^>]+>")
        return tag.sub("", text)

    with tracer.start_span("get-nation-api") as span:
        res = requests.get("https://api.nationalize.io/?name=nathaniel")
        span.log_kv({"event": "get count", "count": len(res.json())})
        span.set_tag("get-count", len(res.json()))

        result_info = []
        result = {}
        for result in res.json():        
            with tracer.start_span("get-nation-api-data") as site_span:
                logger.info(f"Getting website for api called")
                try:
                    site_span.set_tag("http.status_code", res.status_code)
                    site_span.set_tag("name", "nation data")
                except Exception:
                    logger.error(f"Unable to get result for cannot call")
                    site_span.set_tag("http.status_code", res.status_code)
                    site_span.set_tag("api_name", "get-nation-api")

    return jsonify(result_info)

@app.before_request
def before_request():
    request.start_time = time.time()
    REQUEST_IN_PROGRESS.labels(method=request.method, path=request.path).inc()

@app.after_request
def after_request(response):
    request_latency = time.time() - request.start_time
    REQUEST_COUNT.labels(method=request.method, status=response.status_code, path=request.path).inc()
    REQUEST_LATENCY.labels(method=request.method, status=response.status_code, path=request.path).observe(request_latency)
    REQUEST_IN_PROGRESS.labels(method=request.method, path=request.path).dec()
    return response

@app.route('/uptime_checker')
def metrics():
    APP_UPTIME.set(time.time() - start_time)
    return generate_latest()

@app.route('/error')
def error():
    return jsonify({"error": "An intentional error occurred!"}), 500

if __name__ == "__main__":
    app.run()
