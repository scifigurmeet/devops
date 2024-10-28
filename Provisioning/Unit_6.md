# Unit 6: Advanced Provisioning and Testing Strategies
### B.Tech Final Year DevOps Engineering

## Table of Contents
1. [Immutable Infrastructure](#1-immutable-infrastructure)
2. [Container Orchestration with Kubernetes](#2-container-orchestration-with-kubernetes)
3. [Serverless Computing](#3-serverless-computing)
4. [Infrastructure Testing](#4-infrastructure-testing)
5. [Chaos Engineering](#5-chaos-engineering)
6. [Performance Testing](#6-performance-testing)
7. [Security Testing in CI/CD](#7-security-testing-in-cicd)
8. [Contract Testing](#8-contract-testing)
9. [Property-Based Testing](#9-property-based-testing)
10. [Mutation Testing](#10-mutation-testing)

## 1. Immutable Infrastructure

### 1.1 Introduction
Immutable infrastructure is a paradigm where servers, once deployed, are never modified in-place. Instead, any change requires creating new infrastructure.

### 1.2 Key Principles
- **No in-place updates**: Servers are never patched or updated directly
- **Version control**: Infrastructure configurations are version controlled
- **Automated deployment**: Complete automation of infrastructure creation
- **Disposable resources**: All resources can be destroyed and recreated easily

### 1.3 Implementation Tools
1. **Packer**
   ```hcl
   source "amazon-ebs" "ubuntu" {
     ami_name      = "my-application-{{timestamp}}"
     instance_type = "t2.micro"
     source_ami    = "ami-0123456789"
     ssh_username  = "ubuntu"
   }

   build {
     sources = ["source.amazon-ebs.ubuntu"]
     
     provisioner "shell" {
       inline = [
         "sudo apt-get update",
         "sudo apt-get install -y nginx"
       ]
     }
   }
   ```

2. **Terraform**
   ```hcl
   resource "aws_instance" "web" {
     ami           = var.ami_id
     instance_type = "t2.micro"
     
     tags = {
       Name = "immutable-web-server"
     }
     
     lifecycle {
       create_before_destroy = true
     }
   }
   ```

### 1.4 Benefits
- Consistency across environments
- Simplified rollback process
- Improved security
- Better disaster recovery
- Reduced configuration drift

## 2. Container Orchestration with Kubernetes

### 2.1 Core Concepts
1. **Pods**: Smallest deployable units
2. **Services**: Network abstraction for pod access
3. **Deployments**: Declarative updates for pods
4. **ConfigMaps & Secrets**: Configuration management

### 2.2 Basic Pod Configuration
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```

### 2.3 Deployment Strategies
1. **Rolling Updates**
   ```yaml
   spec:
     strategy:
       type: RollingUpdate
       rollingUpdate:
         maxSurge: 1
         maxUnavailable: 0
   ```

2. **Blue-Green Deployments**
3. **Canary Releases**

### 2.4 Service Types
- ClusterIP
- NodePort
- LoadBalancer
- ExternalName

## 3. Serverless Computing

### 3.1 Concepts
- Function as a Service (FaaS)
- Event-driven architecture
- Auto-scaling
- Pay-per-use pricing

### 3.2 AWS Lambda Example
```python
import json

def lambda_handler(event, context):
    # Parse input
    body = json.loads(event['body'])
    
    # Process data
    result = process_data(body)
    
    # Return response
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

### 3.3 Use Cases
1. API backends
2. Data processing
3. Scheduled tasks
4. Real-time file processing
5. Stream processing

### 3.4 Limitations
- Cold starts
- Maximum execution time
- Memory constraints
- State management

## 4. Infrastructure Testing

### 4.1 TestInfra
```python
def test_docker_service(host):
    docker = host.service("docker")
    assert docker.is_running
    assert docker.is_enabled

def test_ports(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening
    assert host.socket("tcp://0.0.0.0:443").is_listening
```

### 4.2 Goss
```yaml
port:
  tcp:80:
    listening: true
    ip: [0.0.0.0]
  tcp:443:
    listening: true
    ip: [0.0.0.0]

service:
  nginx:
    enabled: true
    running: true
```

### 4.3 Testing Strategies
1. Configuration validation
2. Service health checks
3. Network connectivity
4. Security compliance
5. Performance benchmarks

## 5. Chaos Engineering

### 5.1 Principles
1. Build a hypothesis
2. Define steady state
3. Introduce real-world events
4. Observe results
5. Improve system

### 5.2 Chaos Monkey Implementation
```java
@Component
public class ChaosMonkey {
    public void terminateRandomInstance() {
        List<EC2Instance> instances = getRunningInstances();
        if (!instances.isEmpty()) {
            Random rand = new Random();
            EC2Instance target = instances.get(rand.nextInt(instances.size()));
            target.terminate();
            notifyTeam("Instance " + target.getId() + " terminated");
        }
    }
}
```

### 5.3 Tools
1. **Chaos Monkey**
   - Netflix's tool for random instance termination
2. **Gremlin**
   - Commercial platform for chaos experiments
3. **Litmus**
   - Kubernetes-native chaos engineering

## 6. Performance Testing

### 6.1 Types
1. **Load Testing**
   ```java
   @Test
   public void loadTest() {
       setUp(
           scenario("Standard load test")
               .exec(http("request")
                   .get("/api/resource"))
               .pause(1)
       ).protocols(http.baseUrl("http://test-api.com"))
        .assertions(
            global().responseTime().mean().lt(100),
            global().successfulRequests().percent().gt(95)
        );
   }
   ```

2. **Stress Testing**
3. **Endurance Testing**
4. **Spike Testing**

### 6.2 Tools
1. **JMeter**
2. **K6**
3. **Gatling**

### 6.3 Metrics to Monitor
- Response time
- Throughput
- Error rate
- Resource utilization
- Concurrent users

## 7. Security Testing in CI/CD

### 7.1 Types of Security Testing
1. **SAST (Static Application Security Testing)**
   ```yaml
   sonarqube:
     stage: test
     script:
       - sonar-scanner \
           -Dsonar.projectKey=$CI_PROJECT_PATH_SLUG \
           -Dsonar.sources=. \
           -Dsonar.host.url=$SONAR_URL \
           -Dsonar.login=$SONAR_TOKEN
   ```

2. **DAST (Dynamic Application Security Testing)**
3. **SCA (Software Composition Analysis)**

### 7.2 Tools
1. SonarQube
2. OWASP ZAP
3. Snyk
4. GitLab Security Scanners

### 7.3 Implementation Best Practices
1. Early integration in pipeline
2. Automated security gates
3. Regular dependency updates
4. Compliance checking

## 8. Contract Testing

### 8.1 Consumer Driven Contracts
```java
@Pact(consumer = "OrderService")
public RequestResponsePact createPact(PactDslWithProvider builder) {
    return builder
        .given("User exists")
        .uponReceiving("A request for user details")
        .path("/api/users/1")
        .method("GET")
        .willRespondWith()
        .status(200)
        .body(new PactDslJsonBody()
            .stringType("name")
            .numberType("age"))
        .toPact();
}
```

### 8.2 Provider Verification
1. State management
2. Request verification
3. Response validation
4. Schema validation

### 8.3 Tools
1. Pact
2. Spring Cloud Contract
3. Postman Contract Testing

## 9. Property-Based Testing

### 9.1 Concepts
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_list_reversal(xs):
    # Property: reversing a list twice gives the original list
    assert list(reversed(list(reversed(xs)))) == xs
```

### 9.2 Benefits
1. Better test coverage
2. Edge case discovery
3. Reduced test maintenance
4. Improved test quality

### 9.3 Implementation Strategies
1. Define properties
2. Generate test data
3. Verify properties
4. Handle edge cases

## 10. Mutation Testing

### 10.1 Concepts
- Code mutations
- Test effectiveness
- Mutation operators
- Mutation score

### 10.2 PIT Example
```xml
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.7.3</version>
    <configuration>
        <targetClasses>
            <param>com.example.*</param>
        </targetClasses>
        <targetTests>
            <param>com.example.*</param>
        </targetTests>
    </configuration>
</plugin>
```

### 10.3 Common Mutations
1. Conditional operators
2. Mathematical operators
3. Return values
4. Method calls

### 10.4 Analysis
- Mutation coverage
- Surviving mutations
- Equivalent mutations
- Test improvements

## Practice Questions

1. What are the key principles of immutable infrastructure and how do they benefit DevOps practices?

2. Compare and contrast different Kubernetes deployment strategies. When would you use each?

3. Describe the implementation of chaos engineering in a microservices architecture. What precautions should be taken?

4. How does contract testing differ from traditional integration testing? Provide examples.

5. Explain the role of property-based testing in ensuring software quality. What are its limitations?

## Further Reading

1. "Infrastructure as Code" by Kief Morris
2. "Kubernetes in Action" by Marko Luksa
3. "Chaos Engineering" by Casey Rosenthal & Nora Jones
4. "Continuous Delivery" by Jez Humble and David Farley
5. "The Art of Software Testing" by Glenford J. Myers

## Assessment Criteria

1. Understanding of core concepts (30%)
2. Practical implementation ability (30%)
3. Tool proficiency (20%)
4. Best practices and security awareness (20%)

Remember: This material is designed to provide both theoretical knowledge and practical skills. Practice implementing these concepts in a test environment to gain hands-on experience.
