# 1. VM Setup Introduction

The Google Cloud CLI lets you manage your Compute Engine resources using the gcloud compute command group. gcloud compute is an alternative to using the cloud console.

Here I'm going to show you how to create a VM, install the tools and do some athentication setup all from the command line.
- [1. VM Setup Introduction](#1-vm-setup-introduction)
  - [1.1. Setting up some variables and default values](#11-setting-up-some-variables-and-default-values)
  - [1.2. Create an instance](#12-create-an-instance)
  - [1.3. SSH setup](#13-ssh-setup)
    - [1.3.1. Generate an SSH key](#131-generate-an-ssh-key)
    - [1.3.2. Connect to VM](#132-connect-to-vm)
      - [1.3.2.1. Typing out ssh command](#1321-typing-out-ssh-command)
      - [1.3.2.2. Using gcloud](#1322-using-gcloud)
      - [1.3.2.3. Create a config file](#1323-create-a-config-file)
  - [1.4. Setting up the VM](#14-setting-up-the-vm)
    - [1.4.1. Anaconda install](#141-anaconda-install)
    - [1.4.2. Docker install](#142-docker-install)
    - [1.4.3. Docker-compose install](#143-docker-compose-install)
    - [1.4.4. Terraform install](#144-terraform-install)
  - [1.5. Link service account with our VM.](#15-link-service-account-with-our-vm)
  - [1.6. Stop VM](#16-stop-vm)

## 1.1. Setting up some variables and default values

Before getting started it's handy to either variablize your project id or set it as the default in gloud.

```bash
 # Create variable MY_PROJECT - use $MY_PROJECT to access.
      export MY_PROJECT=literally-my-first-de-project

 # Set default project id.
    export CLOUDSDK_CORE_PROJECT=<PROJECT_ID>
```

Now you can get some info on your project.

```bash
# Describe project
      gcloud compute project-info describe --project <PROJECT_ID>

# View project configurations
        cloud config list
```

Next it is also nice to set your region and zone to a default.  To see your default zone and region. If output is *unset* then no default exists.  

```bash
# View your default region
    gcloud config get-value compute/region

# View your default zone
    gcloud config get-value compute/zone
```

Before setting a default you may want to have a look at the options.

```bash
# View your default region
    gcloud compute regions list

# View your default zone
    gcloud compute zone list

# If you want some more detail on a zone or region.
    gcloud compute zones describe <ZONE>
```

There are 3 ways to set the region and zone and if I'm not mistaken there's a heierarchy:

1. **In the metadata server.** The default region and zone set in the metadata server are applied to your local client when you run gcloud init.

2. **In your local client.** The default region and zone set in your local client override the default region and zone set in the metadata server.

3. **In environment variables.** The default region and zone set in environment variables override the default region and zone set in your local client and in the metadata server.

> You can override any of the above by providing --region and --zone flags when you run commands.

```bash
# Set region
    gcloud config set compute/region <REGION>

# To confirm setting
    gcloud config get-value compute/region

# Unset region
    gcloud config unset compute/region

# Set zone
    gcloud config set compute/region <ZONE>

# To confirm setting
    gcloud config get-value compute/zone

# Unset zone
    gcloud config unset compute/zone
```

I went with these settings.

```bash
 # My region
    gcloud config set compute/region northamerica-northeast1

# My zone
      gcloud config set compute/zone northamerica-northeast1-a
```

For more info on setting region and zone click see the [gcloud docs](https://cloud.google.com/compute/docs/gcloud-compute).

## 1.2. Create an instance

When Alexey showed the cli commands for creating a VM that shit looked scary right?  After digging into the docs a bit I realized the majority of that paragraph belongs to the --create-disk flag and a lot of it is default values.  I tried to boil it down and make some sense of it.

Now most of it now makes sense.  The longest part `image=projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20220419` is like a path I think? Kind of.

Check it out:

```bash
# List images
    gcloud compute images list
```

When you scroll down you see :

  - `NAME=ubuntu-2004-focal-v20220419`
  - `PROJECT=ubuntu-os-cloud`
  - `FAMILY=ubuntu-2004-lts`.

So you can see most of where `image=projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20220419` comes from.

Having said all that it helps demystify things if you get some help on the create command.

```bash
# Create instance help
    gcloud compute instances create --help
```

Here is my boiled down version:

```bash
# Boiled down VM instance creation with the CLI.
    gcloud compute instances create de-zoomcamp-instance1 --project=$MY_PROJECT --machine-type=e2-standard-4 --create-disk=boot=yes,image=projects/ubuntu-os-cloud/global/images/ubuntu-2004-focal-v20220419,size=30GB,type=projects/$MY_PROJECT/zones/$(gcloud config get-value compute/zone)/diskTypes/pd-balanced
```

And you know what? It works buuuuut it throws a `WARNING`: 

```bash
# The warning
WARNING: Some requests generated warnings:
 - Disk size: '30 GB' is larger than image size: '10 GB'. You might need to resize the root repartition manually if the operating system does not support automatic resizing.
 ```

However I double checked by creating the instance in the console and using the cli the console generated and the same warning occured so I guess we just ignore warnings like a true programmer.

To confirm you can get the details of your compute instance.

```bash
# Get info about VM
    gcloud compute instances describe de-zoomcamp-instance1
```

> Note the natIP, this is the public IP used to ssh in the coming steps.

You can now start and stop the instance from the command line.

```bash
# Start VM
    gcloud compute instances start de-zoomcamp-instance1

# Stop VM
    gcloud compute instances stop de-zoomcamp-instance1
```

## 1.3. SSH setup

Now to connect to our VM we need to setup ssh.  

> Secure Shell Protocol (SSH) is a cryptographic network protocol for operating network services securely over an unsecured network.

First need to generate a ssh key.  ssh-key gen is a terminal command and you can read about it using man ssh-keygen.  My favorite part was:

> Don't use simple sentences or otherwise easily guessable phrases - English prose has only 1-2 bits of entropy per character, and provides very bad passphrases.

You know when someone is talking how your brain can guess the next word based on the context and the previous words in the sentance..... I'm not 100% sure btu that was my big take away.

### 1.3.1. Generate an SSH key

```bash
# You need to be in the .ssh folder of your home directory.
    cd ~/.ssh

# Generate ssh key.
    ssh-keygen -t rsa -f gcp -C william -b 2048

# -t = type of key, -f = filename, -C = comment, -b = bits
```

### 1.3.2. Connect to VM

Now you can SSH into you VM.  The following is a list of ways to connect arranged in ascending levels of cool.

#### 1.3.2.1. Typing out ssh command

```bash
 # Full CLI command
    ssh -i ~/.ssh/gcp william@35.203.71.163
```

#### 1.3.2.2. Using gcloud

This will create another ssh key in you .ssh directory :
    - google_compute_engine
    - google_compute_engine.pub

```bash
# The full glcoud command
    gcloud compute ssh <INSTANCE NAME> --zone <MY ZONE>  --project <MY_PROJECT> 

# gcloud with defaults for you project set.
    gcloud compute ssh de-zoomcamp-instance1
```

#### 1.3.2.3. Create a config file

```bash
# Navigate to your .ssh directory.
    cd ~/.ssh

# Create a file named config.
    touch config

# Open config file.
    vim config or nano config

# Add settings to config file.
    Host <whatever name you want i.e. de-zoompcamp>
        Hostname <external ip>
        User <user name, I think can be anything>
        IdentityFile <path to private ssh key i.e. ~/.ssh/gcp>

# Use to ssh into your machine
    ssh de-zoomcamp

# Real nice right?!
```

## 1.4. Setting up the VM

Now we are going to install some stuff on the fresh VM so we have some tools to work with.  To be clear you should be connected to your VM for these setup steps.  You can't setup you VM if you're not working on it right?  Well maybe there's  a way but you get my point.

We will install:

    - Anaconda
    - Docker
    - Docker compose
    - Terraform

### 1.4.1. Anaconda install

```bash
# Download the anaconda installer
    wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh

# Install
    sh Anaconda3-2021.11-Linux-x86_64.sh

# Continue to follow the prompts for install.
```

### 1.4.2. Docker install

```bash
# Update packages.  IF you don't run this you will get an error.
    sudo apt-get update

# Get docker
    sudo apt-get install docker.io

# Check if docker is installed.  You should see some docker documentation.
    docker
```

Setup a group and add yourself to it.  I honestly don't know exactly what this is and it wasn't really well explained. Alexey just goes to a github repo and follows some instructions.  They are as follows.

```bash
#  Create group - output -> 'Groupadd: group 'docker' already exists'.
    sudo groupadd docker

# Add user to group - output -> 'Adding user william to group docker'.
    sudo gpasswd -a $USER docker

# Restart docker.
    sudo service docker restart

# You need to disconnect/reconnect to the VM.

# Run hello-world - badda bing badda boom right?
    docker run hello-world
```

### 1.4.3. Docker-compose install

We will use instructions from the [docker website](https://docs.docker.com/compose/cli-command/#install-on-linux).

```bash
# Define variable.
    DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}

# Make a directory named cli-plugins.
    mkdir -p $DOCKER_CONFIG/cli-plugins

# Download the docker-compose file.
    curl -SL https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose

# Apply executable permissions to the binary.
    chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
```

Now docker compose needs to be added to the PATH.

```bash

    # Open bashrc in editor.
    vim ~/.bashrc

    # Scroll to bottom and below the `conda initalize` and add:
    export PATH="${HOME}/.docker/cli-plugins:${PATH}"

    # Re-source basrc
    source ~/.bashrc

    # Test it out.
    docker-compose version

# Boom!
```

### 1.4.4. Terraform install 

```bash
# Define variable
    TERRAFORM_CONFIG=${TERRAFORM_CONFIG:-$HOME/.terraform}

# Make a directory named cli-plug-ins.
    mkdir -p $TERRAFORM_CONFIG/cli-plugins/terraform

# Download Terraform zip
    wget https://releases.hashicorp.com/terraform/1.1.9/terraform_1.1.9_linux_amd64.zip -o $TERRAFORM_CONFIG/cli-plugins

# Install unzip
    sudo apt-get install unzip

# Unzip Terraform zip
    unzip $TERRAFORM_CONFIG/cli-plugins/terraform_1.1.9_linux_amd64.zip

# Remove Terraform zip file
    rm terraform_1.1.9_linux_amd64.zip

# Add terraform to .bashrc

# Open bashrc in editor.
    vim ~/.bashrc

    # Scroll to bottom and below the `conda initalize` and add:
    export PATH="${HOME}/.terraform/cli-plugins:${PATH}"

    # Re-source basrc
    source ~/.bashrc

    # Test it out.
    terrafrom -version

# Boom
```

## 1.5. Link service account with our VM.

```bash
# Naviagte to where your service key lives.  The one you created when setting up google cloud - should be a json file. Once in the folder that contains your key:
    sftp de-zoomcamp

# Once on the VM I created a directory for the keys
    mkdir .keys

# Transfer key file
    put <key file name>
```

Now your service account key should be on the VM.

Next SSH back to the machine to validate Vm connection to service account.

```bash
# Connect to VM.
    ssh de-zoomcamp

# Create a variable with account key.
    export GOOGLE_APPLICATION_CREDENTIALS=<PATH TO KEY>

# Authenticate
    gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

# Boom!
```

I didn't clone a repo so I actually sftp'd my terraform folder.  The gist is I created a folder for week 1 on the VM and sftp my terraform folder to that location.  I'm mostly mentioning this because the command actually throws an error saying 'terrafom is not a regular file'.  You need to use a -r (recursive) flag because its a folder.

```bash
# Trasfer terraform files
    put -r terraform
```

Now you can run terrafrom commands on the VM - init, apply, etc.

## 1.6. Stop VM

**DON'T FORGET TO STOP YOUR VM!**

So you don't incure charges while not using your machine you should stop it.

```bash
# Stop VM
    gcloud compute instances stop de-zoomcamp-instance1
```
