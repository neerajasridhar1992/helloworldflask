variable "project_id" {
  description = "The ID of the GCP project."
  type        = string
  default     = "<YOUR_PROJECT_NAME>"
}

variable "region" {
  description = "The region to deploy resources in."
  type        = string
  default     = "us-west2"
}
