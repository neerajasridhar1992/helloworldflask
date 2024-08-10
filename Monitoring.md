# **Monitoring**

## **Why these?**

**Chosen Monitoring Solution:** 
  I would use Google Cloud Monitoring and Logging for monitoring System Metrics & Prometheus Client for Application Metrics.

**Reason for Choosing Google Cloud Monitoring and Logging:**
- Google Cloud Monitoring and Logging is natively integrated with both GKE and Cloud SQL, simplifying the setup/management without additional tooling.
- Google Cloud Monitoring already gives comprehensive metrics for GKE, such as CPU and memory usage, pod status, and network traffic. Cloud Logging further detailed logs from our application and infrastructure. These were useful even while I was trying to get the deployment functional.
- Google Cloud's monitoring and logging services has proven to be scalable and reliable, ensuring effective monitoring as applications grow.
- I could define a HPA to automatically scale the deployment based on load(CPU/Memory)


**Reason for Choosing Prometheus Client:**
 - Prometheus is an open-source monitoring solution that is widely adopted in the industry. It has a large community, extensive documentation, and is compatible with many monitoring and visualization tools like Grafana.
 - Prometheus is designed for real-time monitoring, providing immediate insights into our application's performance. The Prometheus client library allows us to track key metrics such as request latency, error rates, and throughput with low overhead.
 - The Prometheus client for Python is easy to use and integrates well with Flask, enabling us to expose metrics with minimal changes to our codebase. It is very easy to set this client up

## **Metrics to Monitor**
   - The focus here is to monitor for four golden signals -  Latency, Traffic, Errors and Saturation.
   - The first three can be achieved using Prometheus, from the application perspective, while the later three can be achieved from the systems perspective through Google Cloud Monitoring.
     
### **Application Metrics:**

#### Request Latency:
  - The time taken to process a request is important and should be monitored.
  - This directly affects customer experience. High latency can indicate performance issues or bottlenecks.
  - Also it is important to be able to track latency for successful requests versus failed requests, since it is better to fail early. 

##### Error Rates:
  - Tracking error rates (e.g., HTTP 5xx errors) helps identify issues with the application that may be causing failures.
  - This metric is extremely important for ensuring application reliability.

##### Request Rate:
  - Monitoring the number of requests per second helps in understanding the application's load and identifying traffic patterns.
  - This paired with the Error Rates can help us determine SLOs and agree on SLAs when applicable.
  - This can also be used as a means to scale using HPA.

#### Metrics endpoint view:
[Metrics server look](https://github.com/neerajasridhar1992/helloworldflask/blob/main/metrics-endpoint.png)

#### **Infrastructure Metrics:**
  - These are viewable in the Metrics Explorer in GCP.
  - These metrics can further be utilized to automatically scale the deployment when under heavy load.

##### CPU Usage:
  - Metric: container/cpu/usage_time and pod/cpu/usage_time
  - High CPU usage usually indicates that the application is under heavy load.
  - By monitoring this metric, we can ensure that your application has enough CPU resources to handle requests efficiently.
  - Also, a HPA can be put in place to scale the deployment based on CPU load.
  - [Sample Container CPU Metrics](https://github.com/neerajasridhar1992/helloworldflask/blob/main/container-cpu-usage.png)

##### Memory Usage:
  - Metric: container/memory/usage and pod/memory/usage
  - Monitoring memory usage helps us detect memory leaks or resource exhaustion.
  - High memory usage may lead to application crashes or degraded performance.
  - Similar to the CPU based Scaling, we can instrument our HPA to scale the deployment based on memory.
  - [Sample Container Memory Metrics](https://github.com/neerajasridhar1992/helloworldflask/blob/main/container-memory-usage.png)

##### Pod Status:
  - I am talking about the pod status while the deployment gets created, and even in general. Kubectl get po gives info about the pod. kubectl descrive pod gives comprehensive info as well. Similar options on Google Cloud monitoring exist as well.

##### Network Traffic:
  - Metric:
    - container/network/received_bytes_count/
    - pod/network/received_bytes_count
    - container/network/sent_bytes_count
    - pod/network/sent_bytes_count
      
  - This helps to identify potential network bottlenecks, which can impact the application's performance.

##### Disk I/O:
  - We can look for Node Volume usage and consumption.
  - High disk I/O can indicate that the application is reading or writing large amounts of data, which might slow down other operations.
  - Monitoring this metric helps in optimizing storage performance.

##### Auto-Scaling Based on Metrics
  To automatically scale the deployment when metrics exceed certain thresholds,  Horizontal Pod Autoscaling (HPA) can be setup. If CPU usage or memory usage exceeds some threshold (80% or so), the HPA can be setup to scale the pods. 


#### **3. Cloud SQL Metrics:**

##### Query Insights:
  - Monitoring query performance metrics (e.g., query execution time) helps in identifying slow queries and optimizing database performance.

##### System Metrics:
  - Tracking the number of connections and connection errors helps in managing database connection pools and ensuring stable connectivity.
  - [Sample DB System Metrics](https://github.com/neerajasridhar1992/helloworldflask/blob/main/database-metrics-system.png)

#### Other Services to Implement
##### 1. Distributed Tracing:
  - Implementing distributed tracing (e.g., using OpenTelemetry or Google Cloud Trace) allows for end-to-end visibility into request flows, helping identify latency issues and performance bottlenecks across services.

##### 2. APM/Synthetic Monitoring:
  - It is useful to setup AP metrics using NewRelic/Datadog or atleast setup Synthetic monitoring using Runscope, or by utilizing the Istio mesh for more insights into network communications. As the applications scale and more microservices are added, it might make sense to setup sa service mesh like Istio to enable monitoring and security.

##### 3. Service-Level Objectives (SLOs) and Service-Level Indicators (SLIs):
  - Defining SLOs and SLIs for our application helps in setting clear performance targets and measuring the application's reliability against those targets.

##### 4. Custom Dashboards/Reporting:
   - Creating custom dashboards tailored to our application's specific needs provides a comprehensive view of metrics and performance, allowing for more effective monitoring and management. We can also define monitors which could trigger alerts through a Alerting tool like Pagerduty when needed. These Dashboards and monitoring should be implemented via IaC for easy maintenance.
     
##### 5. Incident Management:
  - We could further setup alerting tools like Pagerduty and incident management tools like FireHydrant to manage incident lifecycles. Incident Life cycle management can be a pain, and ensuring we handle all events from grouping alerts in an incident, to managing incident response to post mortem analysis to root cause analysis is important.
