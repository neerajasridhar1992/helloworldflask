## **Monitoring**

**Chosen Monitoring Solution:** 
Google Cloud Monitoring and Logging(System Metrics) & Prometheus Client(Application Metrics)

**Reason for Choosing Google Cloud Monitoring and Logging:**
1. Google Cloud Monitoring and Logging are natively integrated with Google Kubernetes Engine (GKE) and Cloud SQL. This integration simplifies the setup and management of monitoring and logging without requiring additional configuration or third-party tools.
2. Google Cloud Monitoring provides comprehensive metrics for GKE, such as CPU and memory usage, pod status, and network traffic. Cloud Logging captures detailed logs from our application and infrastructure, allowing for in-depth troubleshooting and analysis.
3. Google Cloud's monitoring and logging services are scalable and reliable, handling large volumes of data and providing high availability. This ensures that you can monitor our applications effectively as they grow.
4. The ability to set up custom dashboards and alerts in Google Cloud Monitoring helps in proactively managing the health and performance of our application. Alerts can notify us of issues before they impact users.

**Reason for Choosing Prometheus Client:**
1. Prometheus is an open-source monitoring solution that is widely adopted in the industry. It has a large community, extensive documentation, and is compatible with many monitoring and visualization tools like Grafana.
2. Prometheus is designed for real-time monitoring, providing immediate insights into our application's performance. The Prometheus client library allows us to track key metrics such as request latency, error rates, and throughput with low overhead.
3. The Prometheus client for Python is straightforward to use and integrates well with Flask, enabling us to expose metrics with minimal changes to our codebase. We can start monitoring our application quickly without complex setup.



### **Metrics to Monitor**
#### **1. Application Metrics:**

##### Request Latency:
Reason: Monitoring the latency of incoming requests helps ensure that the application is responding in a timely manner. High latency can indicate performance issues or bottlenecks.
##### Error Rates:
Reason: Tracking error rates (e.g., HTTP 5xx errors) helps identify issues with the application that may be causing failures. This metric is crucial for maintaining application reliability.
##### Request Rate:
Reason: Monitoring the number of requests per second can help in understanding the application's load and identifying traffic patterns. It also aids in scaling decisions.
Metrics endpoint view:
![Uploading Screenshot 2024-08-10 at 1.15.43 AM.png…]()

#### **2. Infrastructure Metrics:**
These metrics can further be utilized to automatically scale the deployment when under heavy load.
##### CPU Usage:
Metric: container/cpu/usage_time
Reason: High CPU usage can indicate that the application is under heavy load. By monitoring this metric, you can ensure that your application has enough CPU resources to handle requests efficiently.

##### Memory Usage:
Metric: container/memory/usage
Reason: Monitoring memory usage helps you detect memory leaks or resource exhaustion. High memory usage may lead to application crashes or degraded performance.

##### Pod Status:
Metric: kubernetes/pod/condition
Reason: Keeping track of pod conditions such as Ready, Scheduled, and Restarted helps ensure that all pods are running as expected and can handle incoming requests.

##### Network Traffic:
Metric: container/network/received_bytes_count and container/network/sent_bytes_count
Reason: Monitoring the volume of network traffic helps in identifying potential network bottlenecks, which can impact the application's performance.

##### Disk I/O:
Metric: container/disk/io_time
Reason: High disk I/O can indicate that the application is reading or writing large amounts of data, which might slow down other operations. Monitoring this metric helps in optimizing storage performance.

##### Auto-Scaling Based on Metrics
To automatically scale your deployment when metrics exceed certain thresholds,  Horizontal Pod Autoscaling (HPA) can be setup. If CPU usage or memory usage exceeds some threshold (80% or so), the HPA can be setup to scale the pods. 


#### **3. Cloud SQL Metrics:**

##### Query Performance:

Reason: Monitoring query performance metrics (e.g., query execution time) helps in identifying slow queries and optimizing database performance.

##### Connection Metrics:

Reason: Tracking the number of connections and connection errors helps in managing database connection pools and ensuring stable connectivity.

#### Other Services to Implement
##### 1. Distributed Tracing:

Reason: Implementing distributed tracing (e.g., using OpenTelemetry or Google Cloud Trace) allows for end-to-end visibility into request flows, helping identify latency issues and performance bottlenecks across services.

##### 2. Error Reporting:

Reason: Using a tool like Google Cloud Error Reporting can help aggregate and analyze application errors, providing insights into error trends and helping prioritize bug fixes.

##### 3. Application Performance Management (APM):

Reason: Implementing APM solutions (e.g., New Relic, Datadog) provides deeper insights into application performance, including transaction traces, code-level insights, and more.

##### 4. Service-Level Objectives (SLOs) and Service-Level Indicators (SLIs):

Reason: Defining SLOs and SLIs for our application helps in setting clear performance targets and measuring the application's reliability against those targets.

##### 5. Custom Dashboards and Reporting:

Reason: Creating custom dashboards tailored to our application's specific needs provides a comprehensive view of metrics and performance, allowing for more effective monitoring and management.
