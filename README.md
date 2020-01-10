# AzureContainerInstanceFileWatcher
Example of a simple file watch and process POC using Docker, Python, and Azure Container Instances

## Overview
This project demonstrates how to use Azure to easily host a containerized application that processes files. This is not intended to be an example of how to create a scalable, production ready system. Instead it shows how to quickly set up a proof of concept of how containers can be run easily in Azure using persistent storage from Azure Files. 

The *dockerfile* will create a container image that when instantiated will monitor a directory for new files that have a certain extension (*.txt in my example). When new files appear with this extension, they are moved to a second directory and the extension *.processed* is added to the end of the filename. This simulates a process that would see new files, process them and write the results to a second location. 

The two directory locations in the container have attached persistent volumes that are Azure Storage File shares. This means other processes can mount the same shares to load files for processing or continue processing. 

## Setup
This project assumes you have an [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/) and [Azure Storage Account](https://docs.microsoft.com/en-us/azure/storage/). 

The *watcher.py* and *watcher.yaml* file assume two file shares are created in the storage account: *watch* and *processed*. These file share should be created in the storage account. 

Next the following values should be updated in *watcher.yaml* to match your settings: 

 * \<your image> - the full name of the image including registry and version (e.g. mydockerregistry.azurecr.io/mycontainer:1.0)
 * \<your server> - name of the login server (e.g. mydockerregistry)
 * \<your username> - username to log into registry
 * \<your password> - password to log into registry
 * \<your storage account> - the name of the storage account
 * \<your account key> - the primary or secondary key for the storage account

## Creating the Docker Image
First build the Docker image:

`docker build -t watcher .`

Then tag and push the image to your registry:

```
docker tag watcher mydockerregistry.azurecr.io/watcher
docker push mydockerregistry.azurecr.io/watcher
```

## Creating the Azure Container Instance
Once *watcher.yaml* is updated, use the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest) to deploy it to Azure:

`az container create --resource-group <your resource group name> --file watcher.yaml`

Once the container is running you can look at the logs using the CLI:

`az container logs --resource-group <resource group name> --name watcher`

To test the process, simply copy a file ending in *.txt* into the *watch* file share (can be done via the portal). The file should be moved to the processed directory and the filename appended with .processed and a message should appear in the logs:
```
Starting watcher on /tmp/watch with target /tmp/send
Processed file: foo2.txt
Processed file: foo3.txt
```
