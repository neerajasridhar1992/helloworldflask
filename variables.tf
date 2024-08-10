variable "project_id" {
  description = "The ID of the GCP project."
  type        = string
  default     = "<project_name>"
}

variable "region" {
  description = "The region to deploy resources in."
  type        = string
  default     = "<region_name>"
}
