# Puppet Master and Agent Docker Setup Guide - Single Folder

This guide walks you through setting up a Puppet Master and Puppet Agent using Docker containers from a single folder, including a practical example of configuration management.

## Prerequisites

- Docker installed and running on your system
- Basic understanding of Docker commands
- Text editor for creating files

## Part 1: Creating Dockerfiles

### Step 1: Create the Puppet Master Dockerfile

Create a `Dockerfile.master` with the following content:

```dockerfile
FROM puppet/puppetserver
EXPOSE 8140
CMD ["foreground"]
```

### Step 2: Create the Puppet Agent Dockerfile

Create a `Dockerfile.agent` with the following content:

```dockerfile
FROM puppet/puppet-agent
CMD ["agent", "--verbose", "--no-daemonize", "--summarize"]
```

## Part 2: Building and Running Containers

### Step 1: Build and Run the Puppet Master Container

Build the Docker image:

```bash
docker build -f Dockerfile.master -t puppet-master .
```

Run the Puppet Master container:

```bash
docker run -d --name puppet -p 8140:8140 puppet-master
```

**Note:** The container is named `puppet` and exposes port 8140 for Puppet communication.

### Step 2: Build and Run the Puppet Agent Container

Build the Puppet Agent image:

```bash
docker build -f Dockerfile.agent -t puppet-agent .
```

Run the Puppet Agent container with a link to the Puppet Master:

```bash
docker run -d --name puppet-agent --link puppet puppet-agent
```

**Note:** The `--link puppet` option connects the agent to the master container.

### Step 3: Verify Container Status

Confirm that both containers are running:

```bash
docker images
docker ps
```

You should see both `puppet-master` and `puppet-agent` images listed, and both containers should be in "Up" status.

## Part 3: Practical Configuration Example

Now let's create a simple Puppet manifest and test the configuration management.

### Step 1: Access the Puppet Master Container

Enter the Puppet Master container:

```bash
docker exec -it puppet /bin/bash
```

### Step 2: Create the Manifest Directory Structure

Create the necessary directory structure for Puppet manifests:

```bash
mkdir -p /etc/puppetlabs/code/environments/production/manifests
```

### Step 3: Create a Simple Puppet Manifest

Create a basic manifest file that will create a "Hello, Puppet!" file on managed nodes:

```bash
cat <<EOF > /etc/puppetlabs/code/environments/production/manifests/site.pp
node default {
  file { '/tmp/hello.txt':
    ensure  => file,
    content => "Hello, Puppet!\n",
  }
}
EOF
```

**Manifest Explanation:**
- `node default` applies this configuration to all nodes
- `file` resource manages a file at `/tmp/hello.txt`
- `ensure => file` ensures the resource exists as a file
- `content` specifies the file contents

### Step 4: Test the Puppet Agent

Run the Puppet agent to apply the configuration:

```bash
docker exec -it puppet-agent puppet agent --test
```

This command will:
- Connect the agent to the master
- Download and apply the manifest
- Show verbose output of the configuration run

### Step 5: Verify the Configuration

Check that the file was created successfully:

```bash
docker exec -it puppet-agent cat /tmp/hello.txt
```

You should see the output: `Hello, Puppet!`

## Understanding the Setup

### Container Communication
- The Puppet Master runs on port 8140
- The `--link` option allows the agent to communicate with the master using the container name `puppet`
- The agent automatically discovers and connects to the master

### Puppet Directory Structure
- `/etc/puppetlabs/code/environments/production/` is the default environment
- `manifests/site.pp` is the main manifest file that defines node configurations
- The `node default` block applies to all agents that don't have specific node definitions

### Testing Process
- `puppet agent --test` performs a one-time configuration run
- The agent contacts the master, downloads the catalog, and applies changes
- Any changes are reported in the output

## Next Steps

Once you have this basic setup working, you can:

1. **Create more complex manifests** with multiple resources
2. **Add modules** for specific applications or services
3. **Configure multiple nodes** with different roles
4. **Set up SSL certificates** for secure communication
5. **Implement Puppet environments** for development, testing, and production

## Troubleshooting

### Common Issues
- **Connection refused:** Ensure the Puppet Master container is running and port 8140 is accessible
- **SSL certificate errors:** Wait a few minutes for the master to generate certificates, or check container logs
- **Permission denied:** Ensure you're running Docker commands with appropriate privileges

### Useful Commands
```bash
# Check container logs
docker logs puppet
docker logs puppet-agent

# Restart containers
docker restart puppet
docker restart puppet-agent

# Clean up (remove containers and images)
docker rm -f puppet puppet-agent
docker rmi puppet-master puppet-agent
```

This guide provides a foundation for understanding Puppet's client-server architecture and configuration management capabilities using Docker containers.
