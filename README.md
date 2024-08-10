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
  * Compute Engine API (`compute.googleapis.com`)  
  * Cloud SQL Admin API (`sqladmin.googleapis.com`)  
  * SQL Component API (`sql-component.googleapis.com`)  
  * Kubernetes Engine API (`container.googleapis.com`)  
  * Cloud Build API (`cloudbuild.googleapis.com`)  
  * Service Networking API (`servicenetworking.googleapis.com`)  
  * IAM API (`iam.googleapis.com`)

### **Explanation of Choices**

* **Terraform:** Terraform was chosen to define the infrastructure as code due to its declarative syntax, support for versioning, and ability to manage a wide range of cloud resources. This approach ensures consistency and repeatability across environments.

* **Docker:** Docker is used to containerize the Flask web application, enabling easy deployment on GKE. Docker ensures that the application runs consistently across different environments by encapsulating all dependencies within the container.

* **CloudSQL Proxy:** Google advises using the CloudSQL Proxy to securely connect applications running in GKE to Cloud SQL instances(Necessary reading involved: https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine](https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine*). This proxy handles authentication and maintains a stable connection, reducing the complexity of managing database connections in a cloud environment.

* **GKE(Autopilot)/Kubernetes:**   
  Why GKE? GKE provides a fully managed Kubernetes service, allowing me to focus on deploying and managing applications without worrying about the underlying infrastructure. Kubernetes is the industry-standard platform for container orchestration, offering robust tools for scaling, load balancing, and self-healing of applications.

* Why Autopilot Mode? Autopilot mode simplifies cluster management by automating many operational tasks, such as node provisioning, scaling, and maintenance, which allows for more focus on application development and deployment rather than infrastructure management.

* **Deployment:** The application is containerized and deployed as a Kubernetes deployment, ensuring that it can run reliably across multiple replicas. The deployment also manages rolling updates, scaling, and the self-healing of pods in case of failure.

* **Service:** A Kubernetes LoadBalancer service is used to expose the application to the internet. It automatically balances incoming traffic across all replicas of the application, ensuring high availability.

## **Application Deployment prep**

**The deployment process involves several key steps:**

1. **Defining the Infrastructure:**
   * Before proceeding with applying the Infrastructure changes, please make the following changes for the code to work as intended:
     * Update the variables.tf file with your project name and region name
     * Update the google_sql_user in the main.tf file, provide your custom username and password for the user.
     * base64 the username and password provided in step ii, and mention the corresponding base64 encoded username and password in the Secret.yaml file.
   * The infrastructure was defined using Terraform and deployed with `terraform apply`.
   * Please update the variables.tf with your project name before proceeding.
   * After deployment, various Google Cloud APIs were enabled to ensure proper functionality of the web application and its integration with other services.  
3. **Developing the Web Application:**  
   * A simple Flask web application was developed locally. The application connects to the Cloud SQL PostgreSQL database to retrieve and display data.  
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
          
        gcloud iam service-accounts keys create credentials.json \--iam-account=sql-access@<project_name>\_ID.iam.gserviceaccount.com

6. **Service Configuration:**  
   * A LoadBalancer service was configured to expose the application, mapping port 80 to the application's container port 5000\.  
   * The service allows external access to the Flask application while balancing traffic across the three replicas. 
 
## **Deployment Process**
The deployment of the Flask web application involves several key steps to ensure it is properly built, containerized, and deployed to GKE:
1. **Building the Docker Image:** After making necessary changes to the `main.py` application, the Docker image is built using the following command. This command builds the Docker image for the Flask application, specifying the platform and tagging it with the appropriate GCR repository.
       `docker build --platform linux/amd64 -t gcr.io/<project-name>/hello-server .`
   
2. **Pushing the Docker Image to Google Container Registry (GCR):** The built Docker image is then pushed to Google Container Registry to make it available for the Kubernetes deployment:

   `docker push gcr.io/<project-name>/hello-server`

3. **Applying Kubernetes Configurations:** The Kubernetes configurations, including ConfigMap, Secrets, and Deployment YAML files, are applied using the following commands. These commands deploy the ConfigMap and Secrets to manage configuration data and sensitive information, respectively, and then apply the Deployment configuration to launch the application in the GKE cluster. Before proceeding, please edit your deployment.yaml with your PROJECT_NAME, REGION_NAME and DATABASE_NAME.

   `kubectl apply -f ConfigMap.yaml`  
   `kubectl apply -f Secrets.yaml`  
   `kubectl apply -f deployment.yaml`
4. **Checking for the app:** The apply should have created your deployment which should have as many pods as defined by the replicas, and each pod should have two containers. The pods were up within 10 mins(less than a min, if just one replica, about 5-6 mins if replicas=2/3). Once the deployment is ready, you can check your GKE workloads for this deployment, drop down to where the UI mentions the Exposing service endpoint, <end-point>, lets say. Open a browser tab and <end-point>/greeting/1, should print Hello-World
## **Challenges & Solutions:**

 i. ***Database Connection Issues:*** Initially, I used the pymysql driver, which is intended for MySQL, while the database was PostgreSQL. This caused connection issues. After realizing the mistake, I switched to a PostgreSQL-compatible driver, ensuring the application could connect to the database successfully.  

 ii. ***Service Account Key Creation:*** While I intended to create the service account keys directly through Terraform, I encountered a JSON marshaling error. To proceed with the project, I temporarily used the gcloud CLI to generate the keys manually. In a production setting, I would resolve this issue to automate the key creation process fully.

### **Monitoring**

To ensure the application runs smoothly and to detect potential issues early, monitoring is a critical aspect of this setup.  
To monitor the application and ensure its reliability, the following approach would be taken:

* **Google Cloud's Operations Suite:** This suite allows for tracking key metrics such as CPU usage, memory consumption, and request latency. Additionally, it provides built-in alerting capabilities to notify when resource usage exceeds predefined thresholds or when other critical events occur.  
* **Prometheus & Grafana:** For more advanced monitoring, Prometheus could be used for collecting metrics, and Grafana for visualizing them through custom dashboards.  
* **OpenTelemetry for Flask:** The OpenTelemetry library can be used to instrument the Flask application for observability. By integrating OpenTelemetry, you can collect traces, metrics, and logs from your application. This helps in gaining comprehensive visibility into application performance and behavior. The collected traces can provide insights into request flows, and performance bottlenecks, and help in debugging issues.  
* **Traces:** OpenTelemetry can track the journey of requests through your application, helping to identify slow components or errors.  
* **Metrics:** Define custom metrics using OpenTelemetry to monitor key performance indicators. These metrics can be used to create Service Level Indicators (SLIs) and, consequently, Service Level Objectives (SLOs).  
* **Logs:** Integrate logging with OpenTelemetry to correlate logs with traces and metrics, providing a unified view of application behavior.  
* **Alerting:** Alerts would be set up to notify of issues like high resource utilization or database connection errors, ensuring timely responses to potential problems.

### **Future Improvements**

* **Automate Service Account Key Creation:** Currently, service account keys were manually generated using the `gcloud` CLI due to a Terraform limitation. As a next step, I would investigate and resolve the Terraform issue to automate this process fully.  
* **Implement TLS:** While not required for this assignment, implementing TLS for secure communication between the client and server would be an important enhancement for a production environment. This would involve using certificates maybe from Google Certificate Authority and defining Ingress, and updating DNS.  
* **Use a Secrets Manager:** To securely manage sensitive information like database credentials, I would integrate a secrets manager such as HashiCorp Vault or Google Secret Manager. This would ensure that secrets are encrypted and managed according to best practices.

