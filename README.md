```
 _____________
< hello world >
 -------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
```
Table Of Contents

   [Infrastructure Overview](README.md#infrastructure-overview)
   
   [Why I chose these?](README.md#explanation-of-choices)
   
   [Deployment Process Explained](README.md#application-deployment-info)

# **Deploying a Flask Web Application on GKE with Cloud SQL and Terraform.**

This project demonstrates a simple Flask web application deployed on Google Kubernetes Engine (GKE) using a Google Cloud SQL PostgreSQL database. The infrastructure is defined and managed using Terraform, ensuring a reproducible and scalable environment. The goal is to demonstrate the ability to deploy a cloud-native application and manage it using modern DevOps practices.

## **Infrastructure Overview**

The infrastructure is composed of the following Google Cloud Platform (GCP) resources, defined via Terraform:

* **GKE Autopilot Cluster:** A managed Kubernetes cluster named `hello-world-cluster`, which hosts the application.  
* **Google Cloud SQL Database:** A managed PostgreSQL database instance that stores and retrieves data for the web application.  
* **Google Service Account:** Used for authenticating and authorizing the application’s interactions with Google Cloud services.  
* **Google Service Account Key:** Created to enable secure communication between the application and the Cloud SQL database via the Cloud SQL Proxy.  
* **Google Project IAM Binding:** Configured to assign necessary roles and permissions to the service account, ensuring it has access to the required Google Cloud resources.  
* **Google Cloud APIs:** Several APIs were enabled to ensure smooth operation and integration between the various services:  
  * Artifact Registry API (`artifactregistry.googleapis.com`)
  * Container Registry API (`containerregistry.googleapis.com`)
  * Compute Engine API (`compute.googleapis.com`)  
  * Cloud SQL Admin API (`sqladmin.googleapis.com`)  
  * SQL Component API (`sql-component.googleapis.com`)  
  * Kubernetes Engine API (`container.googleapis.com`)  
  * Cloud Build API (`cloudbuild.googleapis.com`)  
  * Service Networking API (`servicenetworking.googleapis.com`)
  * Network Connectivity API (`networkconnectivity.googleapis.com`)
  * IAM API (`iam.googleapis.com`)

### **Explanation of Choices**

* **Terraform:** Terraform was chosen to define the infrastructure as code due to its declarative syntax, support for versioning, and ability to manage a wide range of cloud resources. This approach ensures consistency and repeatability across environments.

* **Docker:** Docker is used to containerize the Flask web application, enabling easy deployment on GKE. Docker ensures that the application runs consistently across different environments by encapsulating all dependencies within the container.

* **CloudSQL Proxy:** Google advises using the CloudSQL Proxy to securely connect applications running in GKE to Cloud SQL instances(Necessary reading involved: https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine](https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine*). This proxy handles authentication and maintains a stable connection, reducing the complexity of managing database connections in a cloud environment.

* **GKE(Autopilot)/Kubernetes:**   
  * Why GKE? GKE provides a fully managed Kubernetes service, allowing me to focus on deploying and managing applications without worrying about the underlying infrastructure. Kubernetes is the industry-standard platform for container orchestration, offering robust tools for scaling, load balancing, and self-healing of applications.

  * Why Autopilot Mode? Autopilot mode simplifies cluster management by automating many operational tasks, such as node provisioning, scaling, and maintenance, which allows for more focus on application development and deployment rather than infrastructure management.

* **Deployment:** The application is containerized and deployed as a Kubernetes deployment, ensuring that it can run reliably across multiple replicas. The deployment also manages rolling updates, scaling, and the self-healing of pods in case of failure.

* **Service:** A Kubernetes LoadBalancer service is used to expose the application to the internet. It automatically balances incoming traffic across all replicas of the application, ensuring high availability.

## **Application Deployment Info**

**The deployment process involves several key steps:**

1. **Defining the Infrastructure:**
The infrastructure was defined using Terraform and deployed with terraform apply.
After deployment, various Google Cloud APIs were enabled to ensure proper functionality of the web application and its integration with other services.

2. **Developing the Web Application:**  
   * A simple Flask web application was developed to work well locally. The application connects to the Cloud SQL PostgreSQL database to retrieve and display data.  
   * The right database driver (`pg8000`) was selected to ensure compatibility with PostgreSQL, after initially attempting to use `pymysql` (which is meant for MySQL).  
4. **Dockerizing the Application:**  
   * The Flask application was containerized using Docker, with environment variables configured to match the GKE environment. This included database connection details.  
   * The Docker image was then pushed to Google Container Registry (GCR) for use in the Kubernetes deployment.  
5. **Defining the Kubernetes Deployment/Secrets/ConfigMaps:**

   * The Kubernetes deployment was configured to use two containers:  
     i. Hello-Server Container: Runs the Flask application, using environment variables (such as database credentials) provided via Kubernetes secrets and ConfigMaps.  

     ii. Cloud SQL Proxy Container: A sidecar container that securely connects the application to the Cloud SQL instance using the service account credentials.  

     iii. Secret.yaml: Database credentials were loaded using Kubernetes Secrets. While Kubernetes Secrets provides base64 encoding for the data, this method is not secure enough for sensitive information. For better security, it is advisable to use a dedicated secrets management solution like HashiCorp Vault or Google Cloud Secret Manager, which offers encryption and more secure handling of sensitive data.  

     iv. Google Service Account Credentials: An environment variable was set up for the Google credentials linked to the service account created via Terraform. These credentials are needed to connect to the Cloud SQL Proxy. The credentials were generated using the following gcloud CLI command:  
          
        `gcloud iam service-accounts keys create credentials.json \--iam-account=sql-access@<project_name>\_ID.iam.gserviceaccount.com`

6. **Service Configuration:**  
   * A LoadBalancer service was configured to expose the application, mapping port 80 to the application's container port 5000\.  
   * The service allows external access to the Flask application while balancing traffic across the three replicas. 
 
## **Deployment Process**
1. **Creating the Infrastructure through Terraform:**
   * Before proceeding with applying the Infrastructure changes, please make the following changes for the code to work as intended:
     * cd to the terraform directory
     * Change your config to point to your project where you will set up all the Infrastructure and Enable all the APIS mentioned as mentioned below, 
       ```
       gcloud config set project <project-name>
       gcloud services enable artifactregistry.googleapis.com
       gcloud services enable containerregistry.googleapis.com
       gcloud services enable compute.googleapis.com
       gcloud services enable sqladmin.googleapis.com
       gcloud services enable sql-component.googleapis.com
       gcloud services enable container.googleapis.com
       gcloud services enable cloudbuild.googleapis.com
       gcloud services enable servicenetworking.googleapis.com
       gcloud services enable networkconnectivity.googleapis.com
       gcloud services enable iam.googleapis.com
       ```
     * Update line 17 in k8s/deployment.yaml with your project name.
     * Update the variables.tf file with your project name and region name.
     * Update the google_sql_user in the main.tf file, provide your custom username and password for the user.
     * base64 the username and password provided in step ii, and mention the corresponding base64 encoded username and password in the k8s/Secret.yaml file.
       `echo <username>| base64`
        `echo <password>| base64`
     *  Initiate the infrastructure with a `terraform init`, check the plan with `terraform plan`.
     *  The infrastructure can now be defined using Terraform and deployed with `terraform apply`. It takes about 10 mins on average to complete creation of a gke cluster and a cloudsql instance.
     *  Once the apply finishes, it will output the cloudsql instance name, please update the <cloudsql_instance_connection_name> in k8s/deployment.yaml at line 27 and 68.
       


2. **Building the Docker Image:**
   * cd to the app directory
   *  Update the `<project-name>` in this command before proceeding. This command builds the Docker image for the Flask application, specifying the platform and tagging it with the appropriate GCR repository.
       `docker build --platform linux/amd64 -t gcr.io/<project-name>/hello-server .`
   
4. **Pushing the Docker Image to Google Container Registry (GCR):**
   * Update the `<project-name>` in this command before proceeding. The built Docker image is then pushed to Google Container Registry to make it available for the Kubernetes deployment:

   `docker push gcr.io/<project-name>/hello-server`

6. **Applying Kubernetes Configurations:** The Kubernetes configurations, including ConfigMap, Secrets, and Deployment YAML files, are applied using the following commands. These commands deploy the ConfigMap and Secrets to manage configuration data and sensitive information, respectively, and then apply the Deployment configuration to launch the application in the GKE cluster.
   * cd to the k8s directory
   * Set the gcloud context to your project:
     `gcloud config set project <project-name>`
   * Gather the email address of the sql-access service account. The following command should gather that for you
     `gcloud iam service-accounts list --project=<projectname> | grep sql-accesss`
   * Please use this command to generate the credentials.json, that is used in the GoogleCredsSecret.yaml:
     `gcloud iam service-accounts keys create credentials.json \--iam-account=<emailofserviceaccount>`
   * The previous command would have created a credentials.json file for you. Replace the empty { } in line 8 and 9 with the contents of credentials.json. Please pay attention to possible indentation errors here, json versus yaml indentation requirements should be taken into consideration.
   * Go ahead and run the following commands in that order to create all the neccesary k8s objects.

   ```
   kubectl apply -f ConfigMap.yaml
   kubectl apply -f GoogleCredsSecret.yaml
   kubectl apply -f Secret.yaml 
   kubectl apply -f deployment.yaml
   ```
8. **Checking for the app:** The apply should have created your deployment which should have as many pods as defined by the replicas, and each pod should have two containers. The pods were up within 10 mins(less than a min, if just one replica, about 5-6 mins if replicas=2/3). Once the deployment is ready, you can check your GKE workloads for this deployment, drop down to where the UI mentions the Exposing service endpoint, `<end-point>`, lets say. Open a browser tab and enter `<end-point>/greeting/1`, should print Hello-World

## **Challenges & Solutions:**

 i. ***Database Connection Issues:*** Initially, I used the pymysql driver, which is intended for MySQL, while the database was PostgreSQL. This caused connection issues. After realizing the mistake, I switched to a PostgreSQL-compatible driver, ensuring the application could connect to the database successfully.  

 ii. ***Service Account Key Creation:*** While I intended to create the service account keys directly through Terraform, I encountered a JSON marshaling error. To proceed with the project, I temporarily used the gcloud CLI to generate the keys manually. In a production setting, I would resolve this issue to automate the key creation process fully.

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

### **Future Improvements**

* **Automate Service Account Key Creation:** Currently, service account keys were manually generated using the `gcloud` CLI due to a Terraform limitation. As a next step, I would investigate and resolve the Terraform issue to automate this process fully.  
* **Implement TLS:** While not required for this assignment, implementing TLS for secure communication between the client and server would be an important enhancement for a production environment. This would involve using certificates maybe from Google Certificate Authority and defining Ingress, and updating DNS.  
* **Use a Secrets Manager:** To securely manage sensitive information like database credentials, I would integrate a secrets manager such as HashiCorp Vault or Google Secret Manager. This would ensure that secrets are encrypted and managed according to best practices.
* **Implement Prometheus Server and Grafana:** To be able to visualize the Application metrics.

