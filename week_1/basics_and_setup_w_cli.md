- [1. Introduction](#1-introduction)
  - [1.1. Project setup](#11-project-setup)
  - [1.2. Create a project](#12-create-a-project)
    - [1.2.1. Base create command](#121-base-create-command)
    - [1.2.2. Create command options](#122-create-command-options)
    - [1.2.3. Create project](#123-create-project)
  - [1.3. Link billing account](#13-link-billing-account)
    - [1.3.1. Check if billing account is linked to project](#131-check-if-billing-account-is-linked-to-project)
    - [1.3.2. List billing accounts - may require installing beta CLI commands](#132-list-billing-accounts---may-require-installing-beta-cli-commands)
    - [1.3.3. Link a billing account](#133-link-a-billing-account)
  - [1.4. Enabling API's](#14-enabling-apis)
    - [1.4.1. Base command.](#141-base-command)
    - [1.4.2. Get a list of available google cloud services - they are numerous.](#142-get-a-list-of-available-google-cloud-services---they-are-numerous)
    - [1.4.3. Enable the IAM API](#143-enable-the-iam-api)
    - [1.4.4. List service accounts](#144-list-service-accounts)
    - [1.4.5. Create variable SA_ID](#145-create-variable-sa_id)
  - [1.5. Create a service account](#15-create-a-service-account)
    - [1.5.1. General considereations when naming a service account](#151-general-considereations-when-naming-a-service-account)
    - [1.5.2. Create service account](#152-create-service-account)
    - [1.5.3. Create a service account key](#153-create-a-service-account-key)
      - [1.5.3.1. Create key](#1531-create-key)
      - [1.5.3.2. Create variable for service account key](#1532-create-variable-for-service-account-key)
    - [1.5.4. Authenticate service account using key](#154-authenticate-service-account-using-key)
  - [1.6. Grant roles to service account](#16-grant-roles-to-service-account)
    - [1.6.1. List roles](#161-list-roles)
    - [1.6.2. Enable Cloud Resource Manager API](#162-enable-cloud-resource-manager-api)
    - [1.6.3. Grant permissions to service account](#163-grant-permissions-to-service-account)
  - [1.7. Assign permissions](#17-assign-permissions)
    - [1.7.1. Storage object admin permissions](#171-storage-object-admin-permissions)
    - [1.7.2. Storage admin permissions](#172-storage-admin-permissions)
    - [1.7.3. Big query admin permissions](#173-big-query-admin-permissions)
# 1. Introduction

I find the google cloud console laggy so I try to do as much in the command line as possible.
As a note taking exercise I decided to translate the first lesson from the DataTalks Club data
engineering course into the command line.

If I'm not mistaken these gcloud instructions aren't applicable to someone who hasn't used google cloud before.  
I'm fairly certain before installing the SDK you need to setup a project and set up a billing account first.
I beleive this is referenced in the documentation but also you need a service account to authenticate your local computer
with google cloud.  Creating a service account requires a project to be created.

- The flow of this document will be:
    1. Project setup.
    2. Linking a billing account.
    3. Enabling API's
    4. Create a service account.
    5. Create a service account key.
    6. Grant roles/permissions to service account.

## 1.1. Project setup

Requirements and some things to consider when choosing a project id and name.

- Project name
  - A human-readable name for your project.
  - The project name isn't used by any Google APIs.
  - You can edit the project name at any time during or after project creation.
  - Project names do not need to be unique.

- Project ID
  - A globally unique identifier for your project.
  - A unique string used to differentiate your project from all others in Google Cloud.
  - You can use the Cloud Console to generate a project ID, or you can choose your own.
  - You can only modify the project ID when you're creating the project.

- Project ID requirements:
  - Must be 6 to 30 characters in length.
  - Can only contain lowercase letters, numbers, and hyphens.
  - Must start with a letter.
  - Cannot end with a hyphen.
  - Cannot be in use or previously used; this includes deleted projects.
  - Cannot contain restricted strings, such as google and ssl.

## 1.2. Create a project

### 1.2.1. Base create command

```bash
        gcloud projects create <PROJECT_ID>
```

### 1.2.2. Create command options

```bash
- --name=NAME

    - Name of the project you want to create.
    - If not specified, will use project id as name.

- --set-as-default 

    - Set newly created project as [core.project] property.

- --enable-cloud-apis

    - Enable cloudapis.googleapis.com during creation. Enabled by default,
    - use --no-enable-cloud-apis to disable.
```

### 1.2.3. Create project

```bash
# Full creat eproject command
        gcloud projects create literally-my-first-de-project --name='de-zoomcamp' --set-as-default

# Create variable MY_PROJECT - use $MY_PROJECT to access
        export MY_PROJECT=literally-my-first-de-project

# Get some project info
        gcloud projects describe $MY_PROJECT
        gcloud config list
```

## 1.3. Link billing account

### 1.3.1. Check if billing account is linked to project

```bash
        gcloud beta billing projects describe $MY_PROJECT
```

### 1.3.2. List billing accounts - may require installing beta CLI commands

```bash
        gcloud beta billing accounts list
```

### 1.3.3. Link a billing account

```bash
        gcloud beta billing projects link <project_name> --billing-account 0X0X0X-0X0X0X-0X0X0X
```

## 1.4. Enabling API's

### 1.4.1. Base command.

```bash
# Base command syntax
        gcloud services enable <SERVICE>
```

### 1.4.2. Get a list of available google cloud services - they are numerous.

```bash
# List enabled services.
        gcloud services list --available --filter <boolean expression>

# Example
        gcloud services list --available --filter='big'
```

### 1.4.3. Enable the IAM API

```bash

#Enable the IAM api
        gcloud services enable iam.googleapis.com
```

### 1.4.4. List service accounts

```bash
        gcloud iam service-accounts list
```

### 1.4.5. Create variable SA_ID

```bash
# Use $SA_ID to access
        export SA_ID=de-zoomcamp-sa
```

## 1.5. Create a service account

### 1.5.1. General considereations when naming a service account

- Service account naming:
  - The ID must be between 6 and 30 characters, and can contain lowercase alphanumeric characters and dashes. 
  - After you create a service account, you cannot change its name.
  - The service account's name appears in the email address that is provisioned during creation in the format SA_NAME@PROJECT_ID.iam.gserviceaccount.com.
  - Each service account also has a permanent, unique numeric ID, which is generated automatically.

- You also provide the following information when you create a service account:
  - SA_DESCRIPTION is an optional description for the service account.
  - SA_DISPLAY_NAME is a friendly name for the service account.
  - PROJECT_ID is the ID of your Google Cloud project.

### 1.5.2. Create service account

```bash
        gcloud iam service-accounts create $SA_ID \ 
        --description="de-zoomcamp-sa" \
        --display-name="de-zoomcamp-sa"
```

### 1.5.3. Create a service account key

- Base command

```bash
# Base command.
        gcloud iam service-accounts keys create
```

- General command syntax
  
```bash
# General command syntax
        gcloud iam service-accounts keys create <key-file> \
        --iam-account=<sa-name>@<project-id>.iam.gserviceaccount.com
```

- Command flags

- key-file
    - The path to a new output file for the private key—for example, ~/sa-private-key.json.
    
- sa-name
    - The name of the service account to create a key for.

- project-id
    - Your Google Cloud project ID.

#### 1.5.3.1. Create key

```bash
        gcloud iam service-accounts keys create ~/Documents/de_zoomcamp/service_account_key.json \
        --iam-account=$SA_ID@$MY_PROJECT.iam.gserviceaccount.com
```

#### 1.5.3.2. Create variable for service account key

```bash
        export GOOGLE_APP_CRED=~/Documents/de_zoomcamp/service_account_key.json
```

### 1.5.4. Authenticate service account using key

You will be redirected to google login

```bash
        gcloud auth application-default login
```

## 1.6. Grant roles to service account

### 1.6.1. List roles

```bash
        gcloud projects get-iam-policy $MY_PROJECT
```

### 1.6.2. Enable Cloud Resource Manager API

```bash
    gcloud services enable cloudresourcemanager.googleapis.com
```

### 1.6.3. Grant permissions to service account

1. General command syntax

```bash
        gcloud <RESOURCE_TYPE> add-iam-policy-binding <RESOURCE_ID> \
        --member=<PRINCIPAL> --role=<ROLE_ID>
```

2. Command options.

- RESOURCE_TYPE
  - The resource type that you want to manage access to. Use projects, resource-manager folders, or organizations.

- RESOURCE_ID
  - Your Google Cloud project, folder, or organization ID. Project IDs are alphanumeric, like my-project.

- PRINCIPAL
  - An identifier for the principal, or member, which usually has the following form: PRINCIPAL_TYPE:ID. For example user:my-user@example.com.

- ROLE_ID
  - The name of the role that you want to grant. For example, roles/resourcemanager.projectCreator
    
## 1.7. Assign permissions

### 1.7.1. Storage object admin permissions

```bash
        gcloud projects add-iam-policy-binding $MY_PROJECT \
        --member="serviceAccount:$SA_ID@$MY_PROJECT.iam.gserviceaccount.com" \
        --role="roles/storage.objectAdmin"
```

### 1.7.2. Storage admin permissions

```bash

        gcloud projects add-iam-policy-binding $MY_PROJECT \
        --member="serviceAccount:$SA_ID@$MY_PROJECT.iam.gserviceaccount.com" \
        --role=roles/storage.admin
```

### 1.7.3. Big query admin permissions

```bash
        gcloud projects add-iam-policy-binding $MY_PROJECT \
        --member="serviceAccount:$SA_ID@$MY_PROJECT.iam.gserviceaccount.com" \
        --role=roles/bigquery.admin
```
