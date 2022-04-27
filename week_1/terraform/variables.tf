locals {
  data_lake_bucket = "dtc_data_lake"
}

variable "project" {
  description = "literally-my-first-de-project"
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "northamerica-northeast1"
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "trips_data_all"
}

variable "TABLE_NAME" {
  description = "BigQuery Table"
  type = string
  default = "ny_trips"
}

variable "bucket_name"{
    description = "Name of gcs bucket"
    default = "de_zoomcamp_bucket"
}