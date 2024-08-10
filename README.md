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

# **Deploying a Flask Web Application on GKE with Cloud SQL and Terraform.**  

This project demonstrates a simple Flask web application deployed on Google Kubernetes Engine (GKE) using a Google Cloud SQL PostgreSQL database. The infrastructure is defined and managed using Terraform, ensuring a reproducible and scalable environment. The components of the app are defined through Docker and K8s to demonstrate effective maintainability,  reusability and scalability.

## **Table Of Contents:**
- [Infrastructure Overview](README.md#infrastructure-overview)
- [Why I chose these?](README.md#explanation-of-choices)
- [Deployment Process Explained](README.md#application-deployment-info)
- [How to deploy this app?](README.md#how-to-get-this-app-running)
- [Challenges](README.md#challenges--solutions)
- [Monitoring](README.md#monitoring)

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

## **Explanation of Choices**

* **Terraform:**
  * Utilized Terraform to define the IaC due to its declarative syntax, support for versioning, and ability to manage a wide range of cloud resources. Mainly because I like Terraform on how it ensures idempotency and repeatability. 

* **Docker:**
  * Used Docker to containerize the Flask web application, to enable deploying it to the GKE cluster, easily by encapsulating all the required dependencies. 

* **CloudSQL Proxy:**
  * For my Flask container to be able to securely connect to my CloudSQL instance, I utilized the CloudSQL Proxy, upon following instructions from [here](https://cloud.google.com/sql/docs/mysql/connect-kubernetes-engine*). Google advises using the CloudSQL Proxy to securely connect applications running in GKE to Cloud SQL instances.

* **GKE(Autopilot)/Kubernetes:**   
  * Used Kubernetes, because it is the industry standard for container orchestration, and I can effectively scale the cluster when needed, and also take care of load balancing and self healing for my application. An Autopilot GKE provides a fully managed Kubernetes service, which means I could focus on deploying and managing applications without worrying about the underlying infrastructure. Especially, I don't have to focus on operational tasks like node provisioning, scaling and such, and focus on application development.


* **Deployment:**
  * The application is deployed as a Kubernetes deployment, so that application scaling, rolling updates and self healing can be automatically managed. 

* **Service:**
  * Used a Kubernetes LoadBalancer service to expose the application to the internet. It automatically balances incoming traffic across all replicas of the application, ensuring high availability.

## **Application Deployment Info**

 * The deployment process involves several key steps. An overview of the steps has been mentioned here, but I speak in detail about the deployment process in Deploy README.

1. **Defining the Infrastructure:**
   - Defined using Terraform and deployed with terraform apply.
   - All the required Google Cloud APIs were enabled to ensure all the GCP services had connectivity and integration across them.

2. **Developing the Web Application:**  
   - I firstly developed a simple Flask app that could run locally, and connect to the  Cloud SQL PostgreSQL database to retrieve and display data.
   - The right database driver (`psycopg2`) was selected to ensure compatibility with PostgreSQL, after initially attempting to use `pymysql` (which is meant for MySQL).
   - Once the local app worked fine, I edited the env variables used by the app to point to the env variables set by my k8s deployment.

3. **Dockerizing the Application:**  
   - Built a Docker image out of the developed  Flask application.
   - The Docker image was then pushed to Google Container Registry (GCR) for use in the Kubernetes deployment.  
4. **Defining the Kubernetes Deployment/Secrets/ConfigMaps:**

   - The Kubernetes deployment was configured to use two containers:
      - Hello-Server Container: Runs the Flask application, using environment variables (such as database credentials) provided via Kubernetes secrets and ConfigMaps(Defined outside the deployment).
      - Cloud SQL Proxy Container: A sidecar container that securely connects the application to the Cloud SQL instance using the service account credentials.
      - Secret.yaml: Database credentials were loaded using Kubernetes Secrets. While Kubernetes Secrets provides base64 encoding for the data, this method is not secure enough for sensitive information. For better security, it is advisable to use a dedicated secrets management solution like HashiCorp Vault or Google Cloud Secret Manager, which offers encryption and more secure handling of sensitive data.
      - Google Service Account Credentials: An environment variable was set up for the Google credentials linked to the service account created via Terraform. These credentials are needed to connect to the Cloud SQL Proxy. The credentials were generated using the following gcloud CLI command:  
          
        `gcloud iam service-accounts keys create credentials.json \--iam-account=sql-access@<project_name>\_ID.iam.gserviceaccount.com`

5. **Service Configuration:**  
   - Configured a LoadBalancer service to expose the application, mapping port 80 to the application's container port 5000.  
   - The service allows external access to the Flask application while balancing traffic across the three replicas. 
 
## **How to get this app running?**
* Explained here: [Deploy Process](https://github.com/neerajasridhar1992/helloworldflask/blob/main/Deploy.md)

## **Challenges & Solutions:**

 i. ***Database Connection Issues:*** Initially, I used the pymysql driver, which is intended for MySQL, while the database was PostgreSQL. This caused connection issues. After realizing the mistake, I switched to a PostgreSQL-compatible driver, ensuring the application could connect to the database successfully.  

 ii. ***Service Account Key Creation:*** While I intended to create the service account keys directly through Terraform, I encountered a JSON marshaling error. To proceed with the project, I temporarily used the gcloud CLI to generate the keys manually. In a production setting, I would resolve this issue to automate the key creation process fully.

 iii. ***Testing Done***: I have tested this whole document and the deployment procedure against a test project in GCP, and things do appear smooth.

## Monitoring
* Discussed about monitoring here: [Monitoring](https://github.com/neerajasridhar1992/helloworldflask/blob/main/Monitoring.md)

### **Future Improvements**

* **Automate Service Account Key Creation:** Currently, service account keys were manually generated using the `gcloud` CLI due to a Terraform limitation. As a next step, I would investigate and resolve the Terraform issue to automate this process fully.  
* **Implement TLS:** While not required for this assignment, implementing TLS for secure communication between the client and server would be an important enhancement for a production environment. This would involve using certificates maybe from Google Certificate Authority and defining Ingress, and updating DNS.  
* **Use a Secrets Manager:** To securely manage sensitive information like database credentials, I would integrate a secrets manager such as HashiCorp Vault or Google Secret Manager. This would ensure that secrets are encrypted and managed according to best practices.
* **Implement Prometheus Server and Grafana:** To be able to visualize the Application metrics.

