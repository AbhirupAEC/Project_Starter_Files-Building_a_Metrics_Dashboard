**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

Done *TODO:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation

## Setup the Jaeger and Prometheus source
Done *TODO:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.

## Create a Basic Dashboard
Done*TODO:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.

## Describe SLO/SLI
Done *TODO:* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.

We may have SLOs such as:

Monthly Uptime: The service should be available 99.9% of the time during a given month.

Request Response Time: 95% of all HTTP requests should complete in under 300ms.

Then the SLIs for these would be:

Availability SLI: The percentage of successful uptime minutes in the month.

Latency SLI: The percentage of requests served within the 300ms threshold.

## Creating SLI metrics.
Done *TODO:* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs. 

To effectively measure these SLIs, we need to track relevant metrics that give us visibility into the service's performance. Here are five important metrics and why they matter:

Uptime/Downtime Tracking

Metric: Total minutes of uptime vs. downtime in a given month.

Why it matters: This directly measures service availability and is the primary metric for the monthly uptime SLO.

Request Latency Percentiles (e.g., p95, p99)

Metric: Response time for the 95th and 99th percentile of requests.

Why it matters: These percentile-based latency measurements tell us how the system performs for the majority of users, and are key to tracking the request response time SLO.

Error Rate

Metric: Percentage of failed HTTP requests (e.g., 5xx errors) over total requests.

Why it matters: High error rates can indicate poor availability or degraded performance, affecting both uptime and latency SLIs.

Traffic Volume

Metric: Number of requests per minute/hour/day.

Why it matters: Understanding traffic patterns helps contextualize uptime and latency metrics, ensuring spikes don't skew the SLI measurements unfairly.

Service Health Checks

Metric: Results from automated probes that simulate user interactions (e.g., synthetic checks).

Why it matters: Provides an independent verification of service uptime from an external user's perspective, which can validate internal uptime calculations.



## Create a Dashboard to measure our SLIs
Done *TODO:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.


## Tracing our Flask App
*TODO:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here. Also provide a (screenshot) sample Python file containing a trace and span code used to perform Jaeger traces on the backend service.
Done: screen shot - span_from_grafana.PNG, span_backend_python_code.PNG

## Jaeger in Dashboards
*TODO:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.
Done: dashboard_using_traces.PNG

## Report Error
*TODO:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue also include a screenshot of the tracer span to demonstrate how we can user a tracer to locate errors easily.

TROUBLE TICKET

Name: Backend code failing

Date: 25/05/2025

Subject: Backend code failing

Affected Area: Backend

Severity: P2

Description: Frontend code while call backend getting 500 error code
Tracer span screen shot: backend_trace_span_showing_error.PNG


## Creating SLIs and SLOs
*TODO:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name four SLIs that you would use to measure the success of this SLO.
To support a Service Level Objective (SLO) of 99.95% uptime per month, we need to define Service Level Indicators (SLIs) that reflect the core aspects of availability and performance. Here are four SLIs we could use:

Availability (Successful Request Rate)

Definition: Percentage of successful requests (e.g., HTTP 200-299 responses) out of total requests.

Why: Directly measures whether users can access the application.

Latency (Request Duration)

Definition: Percentage of requests that complete within a specified time threshold (e.g., 95% of requests under 300ms).

Why: Even if the service is technically "up", if it's too slow, it may be perceived as unavailable.

Error Rate

Definition: Percentage of failed requests (e.g., HTTP 5xx errors or custom application-level errors) over total requests.

Why: High error rates can indicate degraded service and impact perceived uptime.

Dependency Availability

Definition: Availability of critical upstream systems (e.g., database, authentication, third-party APIs).

Why: If a dependency fails, it often leads to the application being perceived as down, even if it's running.

These SLIs together give a well-rounded picture of whether the application meets the 99.95% uptime SLO from both a system and user perspective.

## Building KPIs for our plan
*TODO*: Now that we have our SLIs and SLOs, create a list of 2-3 KPIs to accurately measure these metrics as well as a description of why those KPIs were chosen. We will make a dashboard for this, but first write them down here.
Done:
1. Request Success Rate (%)
Description: The percentage of total requests that return a successful status code (e.g., HTTP 200–299).

Why Chosen: This KPI directly reflects Availability SLI and is the most straightforward measure of whether the application is functioning correctly from the user’s perspective.

2. Request Latency (ms)
Description: The 95th percentile of request response times, measured over short intervals (e.g., per minute).

Why Chosen: This supports the Latency SLI by identifying if a significant portion of users experience slow responses, even if the average latency is acceptable. It helps detect performance degradation early.

3. Error Rate (%)
Description: The percentage of requests that return an error (e.g., 5xx responses or app-level failures).

Why Chosen: This KPI tracks the Error Rate SLI and helps identify system instability or failure trends that could lead to a breach in the SLO.

## Final Dashboard
*TODO*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  
Done: Dashboard screenshot: final_dashboard.PNG, here i have captured the following Request Success Rate, Request Latency, Error Rate using this the required KPIs can be identified
