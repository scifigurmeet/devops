# Beginner's Guide: ELK Stack with Docker Compose on Windows 11

This guide will walk you through setting up a basic ELK (Elasticsearch, Logstash, Kibana) stack using Docker Compose on Windows 11. We'll create a simple setup that ingests a sample log file and visualizes it in Kibana.

## Prerequisites

- Windows 11
- Docker Desktop installed and running

## Step 1: Create a project directory

1. Open Command Prompt or PowerShell
2. Create a new directory for your project:
   ```
   mkdir elk-stack-demo
   cd elk-stack-demo
   ```

## Step 2: Create a docker-compose.yml file

Create a file named `docker-compose.yml` in your project directory with the following content:

```yaml
version: '3.7'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
    ports:
      - 9200:9200
    volumes:
      - elasticsearch-data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:7.14.0
    container_name: logstash
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml
    ports:
      - 5000:5000
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:7.14.0
    container_name: kibana
    ports:
      - 5601:5601
    depends_on:
      - elasticsearch

volumes:
  elasticsearch-data:
```

## Step 3: Configure Logstash

1. Create a `logstash` directory in your project folder:
   ```
   mkdir logstash
   mkdir logstash\config
   mkdir logstash\pipeline
   ```

2. Create a file named `logstash.yml` in the `logstash\config` directory:
   ```yaml
   http.host: "0.0.0.0"
   xpack.monitoring.elasticsearch.hosts: [ "http://elasticsearch:9200" ]
   ```

3. Create a file named `logstash.conf` in the `logstash\pipeline` directory:
   ```
   input {
     file {
       path => "/usr/share/logstash/logs/sample.log"
       start_position => "beginning"
     }
   }

   output {
     elasticsearch {
       hosts => ["elasticsearch:9200"]
       index => "sample-logs-%{+YYYY.MM.dd}"
     }
   }
   ```

## Step 4: Create a sample log file

Create a file named `sample.log` in your project directory with some sample log entries:

```
2023-08-07 10:15:30 INFO User logged in
2023-08-07 10:16:45 ERROR Failed to process request
2023-08-07 10:17:20 WARN Disk space running low
2023-08-07 10:18:10 INFO New user registered
```

## Step 5: Start the ELK stack

1. Open Command Prompt or PowerShell in your project directory
2. Run the following command:
   ```
   docker-compose up -d
   ```

## Step 6: Access Kibana

1. Open a web browser and navigate to `http://localhost:5601`
2. Wait a few minutes for Elasticsearch and Kibana to fully start up

## Step 7: Create an index pattern in Kibana

1. In Kibana, go to Management > Stack Management > Index Patterns
2. Click "Create index pattern"
3. Enter "sample-logs-*" as the index pattern
4. Click "Next step"
5. Select "@timestamp" as the Time field
6. Click "Create index pattern"

## Step 8: Visualize logs in Kibana

1. Go to Discover in the main menu
2. Select your "sample-logs-*" index pattern
3. You should now see your sample log entries

Congratulations! You've successfully set up a basic ELK stack using Docker Compose on Windows 11.

## Troubleshooting

- If you don't see any logs in Kibana, ensure that the `sample.log` file is in the correct location and that Logstash has permission to read it.
- Check the container logs using `docker-compose logs` to see if there are any error messages.

Remember to stop your containers when you're done:

```
docker-compose down
```

This will stop and remove the containers, but preserve the Elasticsearch data volume.
