## Exercise 1: Understanding Cloud Providers and Deployment Models through Networking

### Intention
To simulate different cloud deployment models using Docker networks, helping you understand how private, public, and hybrid clouds operate from a networking perspective.

### Objective
Create and interact with Docker networks to simulate private, public, and hybrid cloud environments, demonstrating network isolation and connectivity.

### Concept Overview
- Private Cloud: A network isolated from external access, used exclusively by one organization.
- Public Cloud: A network that's accessible from the internet, shared by multiple tenants.
- Hybrid Cloud: A combination of private and public cloud resources, allowing some resources to be isolated while others are publicly accessible.

### Steps

1. Create the cloud networks:

```powershell
# Create a "private cloud" network
docker network create --subnet=172.18.0.0/16 private-cloud

# Create a "public cloud" network
docker network create --subnet=172.19.0.0/16 public-cloud

# Create a "hybrid cloud" network
docker network create --subnet=172.20.0.0/16 hybrid-cloud
```

2. Create containers in these networks:

```powershell
# Private cloud container
docker run -d --name private-app --network private-cloud nginx

# Public cloud container
docker run -d --name public-app --network public-cloud -p 8080:80 nginx

# Hybrid cloud containers
docker run -d --name hybrid-app1 --network hybrid-cloud nginx
docker run -d --name hybrid-app2 --network hybrid-cloud nginx
docker network connect public-cloud hybrid-app2
```

3. Test network isolation:

```powershell
# Create a test container in the private network
docker run -it --name test-private --network private-cloud alpine sh

# Inside the test-private container, try to ping other containers
ping private-app
ping public-app
ping hybrid-app1
ping hybrid-app2

# Exit the container
exit

# Create a test container in the public network
docker run -it --name test-public --network public-cloud alpine sh

# Inside the test-public container, try to ping other containers
ping private-app
ping public-app
ping hybrid-app1
ping hybrid-app2

# Exit the container
exit
```

4. Demonstrate hybrid connectivity:

```powershell
# Create a test container in the hybrid network
docker run -it --name test-hybrid --network hybrid-cloud alpine sh

# Inside the test-hybrid container, try to ping other containers
ping private-app
ping public-app
ping hybrid-app1
ping hybrid-app2

# Exit the container
exit
```

### Interpretation
- Private Cloud (private-cloud network):
  - Containers in this network can communicate with each other but are isolated from other networks.
  - This simulates a private cloud where resources are not accessible from outside the organization.

- Public Cloud (public-cloud network):
  - Containers in this network can communicate with each other.
  - The public-app container has a port exposed (8080), simulating a public-facing service.
  - In a real public cloud, resources would be accessible over the internet, which we simulate with the exposed port.

- Hybrid Cloud (hybrid-cloud network + connections):
  - hybrid-app1 is only in the hybrid network, simulating a private resource in a hybrid setup.
  - hybrid-app2 is connected to both hybrid and public networks, simulating a resource that can communicate across both private and public environments.

### Innovative Exercise: Network Isolation and Bridging

1. Create a bridge network:

```powershell
docker network create --subnet=172.21.0.0/16 bridge-network
```

2. Create a container that acts as a bridge:

```powershell
docker run -d --name bridge-app --network bridge-network nginx
docker network connect private-cloud bridge-app
docker network connect public-cloud bridge-app
```

3. Test connectivity through the bridge:

```powershell
# Create a test container in the private network
docker run -it --name test-bridge-private --network private-cloud alpine sh

# Inside the test-bridge-private container, try to ping containers
ping private-app  # Should work
ping public-app   # Should fail
ping bridge-app   # Should work

# Use the bridge to reach the public network
ping -c 1 bridge-app  # Note the IP address
ping -c 1 172.19.0.2  # Use the IP of public-app (check with docker inspect public-app)

# Exit the container
exit
```

### Discussion
- How does the network isolation in this exercise reflect real-world cloud security practices?
- In what scenarios would a hybrid cloud model be beneficial?
- How does the bridge network demonstrate the concept of network peering in cloud environments?

This exercise demonstrates how different cloud models handle network isolation and connectivity. The private cloud is completely isolated, the public cloud is accessible (simulated by the exposed port), and the hybrid cloud shows how resources can span both private and public environments. The bridge network exercise further illustrates how connections between different cloud environments can be carefully controlled and managed.
