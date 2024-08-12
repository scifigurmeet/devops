# End User Monitoring: Practical Exercises for Beginners

## Introduction
This document provides a series of practical exercises to help beginners understand and implement various aspects of end user monitoring. These exercises cover real user monitoring, synthetic transaction monitoring, and server-side monitoring using Python and popular tools.

## Exercise 1: Basic Real User Monitoring with JavaScript

**Objective**: Implement a simple real user monitoring script to track page load time.

1. Create a new HTML file named `index.html` with the following content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RUM Example</title>
</head>
<body>
    <h1>Real User Monitoring Example</h1>
    <p>This page demonstrates basic real user monitoring.</p>

    <script>
        // RUM script will go here
    </script>
</body>
</html>
```

2. Add the following JavaScript code inside the `<script>` tag:

```javascript
window.addEventListener('load', function() {
    const pageLoadTime = performance.now();
    console.log(`Page load time: ${pageLoadTime.toFixed(2)} milliseconds`);
    
    // In a real-world scenario, you'd send this data to your analytics server
    // For this exercise, we'll just log it to the console
});
```

3. Open the HTML file in a web browser and check the console to see the page load time.

## Exercise 2: Synthetic Transaction Monitoring with Python and Selenium

**Objective**: Create a simple synthetic monitoring script to check website availability and performance.

1. Install required packages:
```
pip install selenium webdriver_manager
```

2. Create a new Python file named `synthetic_monitor.py` with the following content:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import time

def check_website(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    start_time = time()
    driver.get(url)
    end_time = time()
    
    load_time = end_time - start_time
    
    print(f"URL: {url}")
    print(f"Status: {'Success' if driver.title else 'Failure'}")
    print(f"Load Time: {load_time:.2f} seconds")
    
    driver.quit()

if __name__ == "__main__":
    websites = [
        "https://www.example.com",
        "https://www.google.com",
        "https://www.github.com"
    ]
    
    for site in websites:
        check_website(site)
        print("---")
```

3. Run the script:
```
python synthetic_monitor.py
```

This script will perform a basic synthetic transaction for each website, checking its availability and measuring load time.

## Exercise 3: Server-Side Monitoring with Python and psutil

**Objective**: Create a simple server monitoring script to track CPU and memory usage.

1. Install required package:
```
pip install psutil
```

2. Create a new Python file named `server_monitor.py` with the following content:

```python
import psutil
import time

def monitor_server():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        print(f"CPU Usage: {cpu_percent}%")
        print(f"Memory Usage: {memory.percent}%")
        print(f"Available Memory: {memory.available / (1024 * 1024):.2f} MB")
        print("---")
        
        time.sleep(5)

if __name__ == "__main__":
    try:
        monitor_server()
    except KeyboardInterrupt:
        print("Monitoring stopped.")
```

3. Run the script:
```
python server_monitor.py
```

This script will continuously monitor and display CPU and memory usage of your system. Press Ctrl+C to stop the script.

## Exercise 4: Exploring Open-Source Monitoring Tools

**Objective**: Familiarize yourself with popular open-source monitoring tools.

1. Set up Prometheus (for server-side monitoring):
   - Download Prometheus from the official website.
   - Configure `prometheus.yml` to scrape metrics from your local machine.
   - Start Prometheus and explore its web interface.

2. Set up Grafana (for visualization):
   - Download and install Grafana.
   - Connect Grafana to your Prometheus instance.
   - Create a simple dashboard to visualize CPU and memory usage.

3. Explore ELK Stack (Elasticsearch, Logstash, Kibana) for log analysis:
   - Set up a basic ELK stack using Docker.
   - Configure Logstash to ingest some sample log files.
   - Use Kibana to search and visualize log data.

## Conclusion

These exercises provide a hands-on introduction to various aspects of end user monitoring. They cover real user monitoring, synthetic transaction monitoring, and server-side monitoring using both custom scripts and popular tools. As you progress, you can expand on these exercises to create more complex monitoring solutions tailored to specific needs.
