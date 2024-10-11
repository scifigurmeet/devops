# Azure Kubernetes Service (AKS) Tutorial

## Introduction

Azure Kubernetes Service (AKS) is a managed container orchestration service provided by Microsoft Azure. It simplifies the deployment, management, and operations of Kubernetes. This tutorial will guide you through the basics of AKS, helping you understand its core concepts and how to get started.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Key Concepts](#key-concepts)
3. [Setting Up AKS](#setting-up-aks)
4. [Deploying an Application](#deploying-an-application)
5. [Scaling and Updating](#scaling-and-updating)
6. [Monitoring and Logging](#monitoring-and-logging)
7. [Best Practices](#best-practices)
8. [Conclusion](#conclusion)

## Prerequisites

Before starting with AKS, ensure you have:

- An active Azure subscription
- Azure CLI installed on your local machine
- kubectl (Kubernetes command-line tool) installed
- Basic knowledge of Docker and Kubernetes concepts

## Key Concepts

Understanding these key concepts is crucial for working with AKS:

- **Cluster**: A set of nodes running containerized applications managed by Kubernetes.
- **Node**: A worker machine (VM) in the Kubernetes cluster.
- **Pod**: The smallest deployable unit in Kubernetes, consisting of one or more containers.
- **Service**: An abstraction that defines a logical set of Pods and a policy to access them.
- **Deployment**: Describes the desired state for Pods and ReplicaSets.

## Setting Up AKS

Follow these steps to set up an AKS cluster:

1. Log in to Azure CLI:
   ```
   az login
   ```

2. Create a resource group:
   ```
   az group create --name myAKSGroup --location eastus
   ```

3. Create an AKS cluster:
   ```
   az aks create --resource-group myAKSGroup --name myAKSCluster --node-count 2 --enable-addons monitoring --generate-ssh-keys
   ```

4. Connect to the cluster:
   ```
   az aks get-credentials --resource-group myAKSGroup --name myAKSCluster
   ```

5. Verify the connection:
   ```
   kubectl get nodes
   ```

## Deploying an Application

Let's deploy a simple application to your AKS cluster:

1. Create a deployment YAML file (e.g., `deployment.yaml`):
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nginx-deployment
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: nginx
     template:
       metadata:
         labels:
           app: nginx
       spec:
         containers:
         - name: nginx
           image: nginx:1.14.2
           ports:
           - containerPort: 80
   ```

2. Apply the deployment:
   ```
   kubectl apply -f deployment.yaml
   ```

3. Expose the deployment as a service:
   ```
   kubectl expose deployment nginx-deployment --type=LoadBalancer --port=80
   ```

4. Check the service status:
   ```
   kubectl get services
   ```

## Scaling and Updating

To scale your application:

```
kubectl scale deployment nginx-deployment --replicas=5
```

To update your application:

1. Edit the deployment YAML file, changing the image version.
2. Apply the changes:
   ```
   kubectl apply -f deployment.yaml
   ```

## Monitoring and Logging

AKS integrates with Azure Monitor for containers:

1. View cluster health:
   ```
   az aks show --resource-group myAKSGroup --name myAKSCluster
   ```

2. Access the Azure portal to view detailed metrics and logs.

## Best Practices

- Use namespaces to organize resources
- Implement proper resource requests and limits
- Regularly update your AKS cluster and applications
- Use Azure Key Vault for managing secrets
- Implement proper network policies
- Use Azure DevOps or GitHub Actions for CI/CD

## Conclusion

This tutorial covered the basics of Azure Kubernetes Service. As you progress, explore more advanced topics like persistent storage, ingress controllers, and advanced networking options. AKS provides a powerful platform for deploying and managing containerized applications at scale.

Remember to clean up resources when you're done experimenting to avoid unnecessary costs:

```
az group delete --name myAKSGroup --yes --no-wait
```

Happy learning and deploying with AKS!
