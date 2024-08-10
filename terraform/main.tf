provider "google" {
  project = var.project_id
  region  = var.region
}
data "google_compute_network" "default_vpc" {
  name = "default"
}
resource "google_container_cluster" "primary" {
  name                = "hello-world-cluster"
  location            = var.region
  enable_autopilot    = true
  deletion_protection = false
}

resource "google_sql_database_instance" "default" {
  name                = "hello-world-db"
  database_version    = "POSTGRES_12"
  region              = var.region
  deletion_protection = false

  settings {
    tier = "db-f1-micro"
    ip_configuration {
      ipv4_enabled        = false  # Disable public IP

      private_network = "projects/my-test-project-432103/global/networks/default"  
    }
  }
}

resource "google_sql_database" "default" {
  name     = "hello_world_db"
  instance = google_sql_database_instance.default.name
}

resource "google_sql_user" "default" {
  name     = "<username>"
  instance = google_sql_database_instance.default.name
  password = "<password>"
}

resource "google_service_account" "cloud_sql_service_account" {
  account_id   = "hellosql"
  display_name = "sql-access"
}

# Bind the Cloud SQL Client role to the Service Account
resource "google_project_iam_binding" "cloud_sql_client_binding" {
  project = var.project_id
  role    = "roles/cloudsql.client"

  members = [
    "serviceAccount:${google_service_account.cloud_sql_service_account.email}",
  ]
}
resource "google_service_account_key" "cloud_sql_key" {
  service_account_id = google_service_account.cloud_sql_service_account.name
  key_algorithm      = "KEY_ALG_RSA_2048"
}

