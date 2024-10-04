# Beginner's Guide to Kubernetes with AKS and EKS

## Introduction to Kubernetes

Kubernetes is an open-source platform for automating deployment, scaling, and management of containerized applications. Before we dive into Azure Kubernetes Service (AKS) and Amazon Elastic Kubernetes Service (EKS), let's understand some basic concepts:

1. **Container**: A lightweight, standalone package that includes everything needed to run a piece of software.
2. **Pod**: The smallest deployable unit in Kubernetes, which can contain one or more containers.
3. **Node**: A worker machine in Kubernetes, part of a cluster.
4. **Cluster**: A set of nodes that run containerized applications managed by Kubernetes.

## Setting Up Your Environment

Before we start, you'll need to set up your environment. Here are the tools you'll need:

1. **Azure CLI** (for AKS) or **AWS CLI** (for EKS)
2. **kubectl**: The Kubernetes command-line tool
3. **Docker**: For building and pushing container images

### Installing Azure CLI (for AKS):

1. Visit the [Azure CLI installation page](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
2. Follow the instructions for your operating system

### Installing AWS CLI (for EKS):

1. Visit the [AWS CLI installation page](https://aws.amazon.com/cli/)
2. Follow the instructions for your operating system

### Installing kubectl:

1. Visit the [kubectl installation page](https://kubernetes.io/docs/tasks/tools/)
2. Follow the instructions for your operating system

### Installing Docker:

1. Visit the [Docker installation page](https://docs.docker.com/get-docker/)
2. Follow the instructions for your operating system

## Azure Kubernetes Service (AKS) Example

We'll deploy a simple Nginx web server on AKS. This will give you a visible application to interact with.

### Step 1: Create an AKS Cluster

1. Open a terminal or command prompt
2. Log in to Azure:
   ```
   az login
   ```
3. Create a resource group:
   ```
   az group create --name myResourceGroup --location eastus
   ```
4. Create an AKS cluster:
   ```
   az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 1 --enable-addons monitoring --generate-ssh-keys
   ```
   This process may take several minutes.

### Step 2: Connect to the Cluster

1. Get the credentials for your cluster:
   ```
   az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
   ```
2. Verify the connection:
   ```
   kubectl get nodes
   ```
   You should see your node listed.

### Step 3: Deploy Nginx

1. Create a file named `nginx-deployment.yaml` with the following content:
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: nginx-deployment
   spec:
     selector:
       matchLabels:
         app: nginx
     replicas: 2
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
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: nginx-service
   spec:
     selector:
       app: nginx
     ports:
       - protocol: TCP
         port: 80
         targetPort: 80
     type: LoadBalancer
   ```
2. Apply the configuration:
   ```
   kubectl apply -f nginx-deployment.yaml
   ```

### Step 4: Access the Nginx Server

1. Get the external IP of the service:
   ```
   kubectl get services
   ```
   Look for the `EXTERNAL-IP` of the `nginx-service`. It may take a few minutes to appear.

2. Once you have the IP, open a web browser and navigate to that IP address. You should see the default Nginx welcome page.

## Amazon Elastic Kubernetes Service (EKS) Example

Now, let's do a similar deployment on EKS.

### Step 1: Create an EKS Cluster

1. Open a terminal or command prompt
2. Configure AWS CLI:
   ```
   aws configure
   ```
   Enter your AWS Access Key ID, Secret Access Key, and preferred region.

3. Create an EKS cluster:
   ```
   eksctl create cluster --name my-cluster --region us-west-2 --node-type t3.micro --nodes 2
   ```
   This process may take 15-20 minutes.

### Step 2: Connect to the Cluster

1. Update your kubeconfig:
   ```
   aws eks update-kubeconfig --name my-cluster --region us-west-2
   ```
2. Verify the connection:
   ```
   kubectl get nodes
   ```
   You should see your nodes listed.

### Step 3: Deploy Nginx

1. Use the same `nginx-deployment.yaml` file we created for AKS.
2. Apply the configuration:
   ```
   kubectl apply -f nginx-deployment.yaml
   ```

### Step 4: Access the Nginx Server

1. Get the external IP of the service:
   ```
   kubectl get services
   ```
   Look for the `EXTERNAL-IP` of the `nginx-service`. It may take a few minutes to appear.

2. Once you have the IP, open a web browser and navigate to that IP address. You should see the default Nginx welcome page.

## Conclusion

You've now deployed the same Nginx server on both AKS and EKS! This demonstrates how Kubernetes can provide a consistent deployment experience across different cloud providers.

Some key things to note:
- The Kubernetes commands (`kubectl`) were the same for both AKS and EKS.
- The main differences were in how we created and connected to the clusters.
- Both services automatically provisioned a load balancer to make our application accessible from the internet.

As you become more comfortable with these basics, you can explore more advanced topics like scaling, updating deployments, and implementing continuous deployment pipelines.
