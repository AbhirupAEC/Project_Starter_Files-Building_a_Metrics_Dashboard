import logging
import re
import requests
from flask import Flask, jsonify, render_template
from flask_opentracing import FlaskTracing
from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from prometheus_flask_exporter import PrometheusMetrics



app = Flask(__name__)

metrics = PrometheusMetrics(app)
# static information as metric
metrics.info("app_info", "Application info", version="1.0.3")

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



if __name__ == "__main__":
    app.run()
