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
