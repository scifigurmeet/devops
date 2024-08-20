# Unit 3: Visualization and Synthetic Monitoring - Lab Practicals

## Introduction

This document contains a series of practical exercises designed for beginners to learn about visualization using Grafana and synthetic monitoring using Selenium and Puppeteer. These practicals are intended for students using Windows 11 PCs with Docker Desktop installed.

## Table of Contents

1. [Grafana Dashboard Creation](#grafana-dashboard-creation)
   - [Practical 1: Setting up Grafana and Creating a Basic Dashboard](#practical-1-setting-up-grafana-and-creating-a-basic-dashboard)
   - [Practical 2: Advanced Grafana Dashboard with Multiple Data Sources](#practical-2-advanced-grafana-dashboard-with-multiple-data-sources)

2. [Synthetic Monitoring](#synthetic-monitoring)
   - [Practical 3: Basic Web Monitoring with Selenium](#practical-3-basic-web-monitoring-with-selenium)
   - [Practical 4: Advanced Web Monitoring with Puppeteer](#practical-4-advanced-web-monitoring-with-puppeteer)

## Grafana Dashboard Creation

### Practical 1: Setting up Grafana and Creating a Basic Dashboard

#### Objective
Set up Grafana using Docker and create a basic dashboard to visualize system metrics.

#### Steps

1. Open PowerShell as Administrator and run the following commands to set up Grafana:

```powershell
# Create a directory for Grafana data
mkdir C:\grafana-data

# Run Grafana container
docker run -d -p 3000:3000 --name=grafana -v C:\grafana-data:/var/lib/grafana grafana/grafana
```

2. Open a web browser and navigate to `http://localhost:3000`.

3. Log in with the default credentials:
   - Username: admin
   - Password: admin

4. Change the password when prompted.

5. Click on "Add your first data source" and select "TestData DB".

6. Click "Save & Test" to ensure the connection is working.

7. Create a new dashboard:
   - Click on the "+" icon in the left sidebar
   - Select "Dashboard"
   - Click "Add new panel"

8. In the query editor:
   - Data source: TestData DB
   - Scenario: Random Walk
   - Series: A

9. Click "Apply" to add the panel to your dashboard.

10. Save the dashboard by clicking the save icon in the top right corner.

#### Interpretation
You've now set up Grafana and created a basic dashboard with random walk data. This simulates real-time data visualization, which is crucial for monitoring system performance and identifying trends.

### Practical 2: Advanced Grafana Dashboard with Multiple Data Sources

#### Objective
Create a more complex dashboard using multiple data sources and visualization types.

#### Steps

1. Add a new data source:
   - Go to Configuration > Data Sources
   - Click "Add data source"
   - Select "Prometheus" (we'll simulate this with another TestData DB)
   - Name it "Simulated Prometheus"
   - Set the URL to `http://localhost:9090` (this is just a placeholder)
   - Click "Save & Test"

2. Create a new dashboard:
   - Click on the "+" icon in the left sidebar
   - Select "Dashboard"

3. Add a Graph panel:
   - Click "Add new panel"
   - Select "Graph"
   - Data source: TestData DB
   - Scenario: Random Walk
   - Series: A, B, C

4. Add a Gauge panel:
   - Click "Add new panel"
   - Select "Gauge"
   - Data source: Simulated Prometheus
   - Metric: random(0, 100)

5. Add a Stat panel:
   - Click "Add new panel"
   - Select "Stat"
   - Data source: TestData DB
   - Scenario: Random Walk
   - Series: D

6. Arrange the panels on your dashboard as desired.

7. Add a dashboard variable:
   - Click the gear icon in the top right to open Dashboard Settings
   - Go to "Variables" and click "Add variable"
   - Name: server
   - Type: Query
   - Data source: TestData DB
   - Query: A,B,C,D

8. Use the variable in your Graph panel:
   - Edit the Graph panel
   - In the query, change the Series to: $server

9. Save the dashboard.

#### Interpretation
This advanced dashboard demonstrates how to use multiple data sources, various visualization types, and dashboard variables. In a real-world scenario, you'd use actual data sources like Prometheus or InfluxDB to monitor real system metrics.

## Synthetic Monitoring

### Practical 3: Basic Web Monitoring with Selenium

#### Objective
Set up a basic synthetic monitoring script using Selenium to check website availability.

#### Steps

1. Install Python and pip if not already installed.

2. Install Selenium and the WebDriver Manager:

```powershell
pip install selenium webdriver-manager
```

3. Create a new file named `selenium_monitor.py` with the following content:

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def check_website(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    start_time = time.time()
    driver.get(url)
    load_time = time.time() - start_time
    
    title = driver.title
    
    driver.quit()
    
    return {
        "title": title,
        "load_time": load_time
    }

# Monitor a website
url = "https://www.example.com"
result = check_website(url)

print(f"Website: {url}")
print(f"Title: {result['title']}")
print(f"Load Time: {result['load_time']:.2f} seconds")
```

4. Run the script:

```powershell
python selenium_monitor.py
```

#### Interpretation
This script uses Selenium to open a website in a headless Chrome browser, measure its load time, and retrieve the page title. This is a basic form of synthetic monitoring that can be used to check website availability and performance.

### Practical 4: Advanced Web Monitoring with Puppeteer

#### Objective
Create a more advanced synthetic monitoring script using Puppeteer to check website functionality.

#### Steps

1. Install Node.js if not already installed.

2. Create a new directory for the project and navigate to it:

```powershell
mkdir puppeteer-monitor
cd puppeteer-monitor
```

3. Initialize a new Node.js project and install Puppeteer:

```powershell
npm init -y
npm install puppeteer
```

4. Create a new file named `puppeteer_monitor.js` with the following content:

```javascript
const puppeteer = require('puppeteer');

async function monitorWebsite(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    const startTime = Date.now();
    await page.goto(url, { waitUntil: 'networkidle0' });
    const loadTime = Date.now() - startTime;
    
    const title = await page.title();
    
    // Check if a specific element exists
    const searchBoxExists = await page.evaluate(() => {
        return !!document.querySelector('input[type="search"]');
    });
    
    // Take a screenshot
    await page.screenshot({ path: 'screenshot.png' });
    
    await browser.close();
    
    return {
        title,
        loadTime,
        searchBoxExists
    };
}

// Monitor a website
const url = 'https://www.example.com';
monitorWebsite(url).then(result => {
    console.log(`Website: ${url}`);
    console.log(`Title: ${result.title}`);
    console.log(`Load Time: ${result.loadTime} ms`);
    console.log(`Search Box Exists: ${result.searchBoxExists}`);
    console.log('Screenshot saved as screenshot.png');
}).catch(err => {
    console.error('Error:', err);
});
```

5. Run the script:

```powershell
node puppeteer_monitor.js
```

#### Interpretation
This Puppeteer script provides more advanced synthetic monitoring capabilities. It not only checks the website's availability and load time but also verifies the presence of specific elements (in this case, a search box) and takes a screenshot. This type of monitoring can be used to ensure that key functionality of a website is working as expected.

## Conclusion

These practicals provide a foundation for understanding and implementing visualization and synthetic monitoring techniques. Grafana dashboards allow for real-time visualization of various metrics, while synthetic monitoring with Selenium and Puppeteer enables automated checking of website availability and functionality. As you become more comfortable with these tools, you can expand on these examples to create more complex monitoring solutions tailored to specific needs.
