# Custom Nagios Plugin Study Guide
## Disk Usage Monitoring Plugin in Docker Container (Windows CMD)

### Overview
This guide walks through creating, deploying, and configuring a custom Nagios plugin to monitor disk usage within a Nagios Docker container running on Windows.

### Prerequisites
- Windows system with Docker Desktop installed
- Running Nagios Docker container
- Basic understanding of Bash scripting and Nagios configuration
- Command Prompt (CMD) access

---

## Part 1: Understanding the Plugin

### Plugin Purpose
The `check_disk_simple.sh` plugin monitors root filesystem usage and returns:
- **OK** (exit 0): Usage ≤ 75%
- **WARNING** (exit 1): Usage 76-90%
- **CRITICAL** (exit 2): Usage > 90%

### Plugin Code Analysis
```bash
#!/bin/bash
USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$USAGE" -gt 90 ]; then
  echo "CRITICAL - Disk usage at ${USAGE}%"
  exit 2
elif [ "$USAGE" -gt 75 ]; then
  echo "WARNING - Disk usage at ${USAGE}%"
  exit 1
else
  echo "OK - Disk usage at ${USAGE}%"
  exit 0
fi
```

**Code Breakdown:**
- `df /` - Shows disk usage for root filesystem
- `awk 'NR==2 {print $5}'` - Extracts usage percentage from second row, fifth column
- `tr -d '%'` - Removes the % symbol for numeric comparison
- Conditional logic checks usage thresholds and exits with appropriate codes

---

## Part 2: Docker Container Setup

### Step 1: Verify Nagios Container is Running
```cmd
docker ps
```
Look for the nagios-monitoring stack and the nagios container within it

### Step 2: Access the Nagios Container
```cmd
docker exec -it nagios /bin/bash
```
*The container name is `nagios` within the `nagios-monitoring` stack*

### Step 3: Navigate to Nagios Directory
```bash
cd /opt/nagios/etc/
```

---

## Part 3: Plugin Creation and Deployment

### Step 4: Create Plugin Directory
```bash
mkdir -p /opt/Custom-Nagios-Plugins
cd /opt/Custom-Nagios-Plugins
```

### Step 5: Create the Plugin File
```bash
cat > check_disk_simple.sh << 'EOF'
#!/bin/bash
USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$USAGE" -gt 90 ]; then
  echo "CRITICAL - Disk usage at ${USAGE}%"
  exit 2
elif [ "$USAGE" -gt 75 ]; then
  echo "WARNING - Disk usage at ${USAGE}%"
  exit 1
else
  echo "OK - Disk usage at ${USAGE}%"
  exit 0
fi
EOF
```

### Step 6: Set Execute Permissions
```bash
chmod +x check_disk_simple.sh
```

### Step 7: Test the Plugin
```bash
./check_disk_simple.sh
```
**Expected Output:** `OK - Disk usage at [XX]%`

---

## Part 4: Nagios Configuration

### Step 8: Define the Command
Navigate to commands configuration:
```bash
cd /opt/nagios/etc/objects/
```

Edit the commands.cfg file:
```bash
nano commands.cfg
```

Add this command definition:
```bash
define command {
    command_name    check_disk_simple
    command_line    /opt/Custom-Nagios-Plugins/check_disk_simple.sh
}
```

### Step 9: Create Service Definition
Edit localhost.cfg:
```bash
nano localhost.cfg
```

Add this service definition:
```bash
define service {
    use                 generic-service
    host_name           localhost
    service_description Root Disk Simple Check
    check_command       check_disk_simple
}
```

### Step 10: Verify Configuration
```bash
/opt/nagios/bin/nagios -v /opt/nagios/etc/nagios.cfg
```
**Expected:** "Things look okay - No serious problems were detected"

---

## Part 5: Restart and Monitor

### Step 11: Restart Nagios Service
```bash
systemctl restart nagios
```
*Or use the method appropriate for your Docker setup*

### Step 12: Exit Container
```bash
exit
```

### Step 13: Access Nagios Web Interface
From Windows CMD, find the container's port mapping:
```cmd
docker port nagios
```

Open browser and navigate to: `http://localhost:[PORT]/nagios`

---

## Part 6: Verification and Troubleshooting

### Verification Steps
1. **Check Plugin Execution:**
   ```bash
   docker exec -it nagios /opt/Custom-Nagios-Plugins/check_disk_simple.sh
   ```

2. **Verify Service Status:**
   - Log into Nagios web interface
   - Navigate to Services → localhost
   - Look for "Root Disk Simple Check"

3. **Check Nagios Logs:**
   ```bash
   docker exec -it nagios tail -f /opt/nagios/var/nagios.log
   ```

### Common Issues and Solutions

**Issue 1: Permission Denied**
```bash
docker exec -it nagios chmod +x /opt/Custom-Nagios-Plugins/check_disk_simple.sh
```

**Issue 2: Plugin Not Found**
- Verify the path in command definition matches actual plugin location
- Check if plugin directory exists and is accessible

**Issue 3: Configuration Errors**
```bash
docker exec -it nagios /opt/nagios/bin/nagios -v /opt/nagios/etc/nagios.cfg
```

**Issue 4: Service Not Appearing**
- Restart Nagios service
- Check for syntax errors in configuration files
- Verify host_name matches your Nagios host configuration

---

## Part 7: Testing Different Scenarios

### Test WARNING State
Create a test version with lower threshold:
```bash
docker exec -it nagios cp /opt/Custom-Nagios-Plugins/check_disk_simple.sh /opt/Custom-Nagios-Plugins/check_disk_test.sh
```

Edit test plugin to trigger WARNING at 50%:
```bash
docker exec -it nagios nano /opt/Custom-Nagios-Plugins/check_disk_test.sh
```

### Test CRITICAL State
Similarly, create a version that triggers CRITICAL at 60%

### Manual Testing
```bash
docker exec -it nagios /opt/Custom-Nagios-Plugins/check_disk_test.sh
```

---

## Part 8: Advanced Configuration

### Adding Performance Data
Modify plugin to include performance data:
```bash
#!/bin/bash
USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$USAGE" -gt 90 ]; then
  echo "CRITICAL - Disk usage at ${USAGE}%|usage=${USAGE}%;75;90;0;100"
  exit 2
elif [ "$USAGE" -gt 75 ]; then
  echo "WARNING - Disk usage at ${USAGE}%|usage=${USAGE}%;75;90;0;100"
  exit 1
else
  echo "OK - Disk usage at ${USAGE}%|usage=${USAGE}%;75;90;0;100"
  exit 0
fi
```

### Setting Custom Check Intervals
In service definition:
```bash
define service {
    use                 generic-service
    host_name           localhost
    service_description Root Disk Simple Check
    check_command       check_disk_simple
    check_interval      5
    retry_interval      1
    max_check_attempts  3
}
```

---

## Part 9: Monitoring and Maintenance

### Regular Monitoring Tasks
1. **Check Plugin Performance:**
   ```bash
   docker exec -it nagios time /opt/Custom-Nagios-Plugins/check_disk_simple.sh
   ```

2. **Monitor Nagios Logs:**
   ```bash
   docker exec -it nagios tail -f /opt/nagios/var/nagios.log | grep "Root Disk Simple Check"
   ```

3. **Backup Configuration:**
   ```cmd
   docker cp nagios:/opt/nagios/etc/objects/commands.cfg ./backup/
   docker cp nagios:/opt/nagios/etc/objects/localhost.cfg ./backup/
   ```

### Plugin Maintenance
- Regularly test plugin functionality
- Update thresholds based on system requirements
- Monitor for false positives/negatives
- Keep backup copies of working configurations

---

## Part 10: Study Questions and Exercises

### Knowledge Check Questions
1. What are the three possible exit codes for Nagios plugins?
2. Why is the `chmod +x` command necessary?
3. What does the `df /` command show?
4. How does Nagios determine if a service is OK, WARNING, or CRITICAL?

### Practical Exercises
1. **Modify Thresholds:** Change WARNING to 80% and CRITICAL to 95%
2. **Multi-Disk Monitoring:** Create a plugin that checks multiple filesystems
3. **Email Notifications:** Configure email alerts for CRITICAL states
4. **Custom Metrics:** Add memory usage monitoring to the plugin

### Advanced Challenges
1. Create a plugin that monitors specific directories
2. Implement trending analysis (compare current vs. historical usage)
3. Add network connectivity checks
4. Create a dashboard widget for disk usage visualization

---

## Conclusion

This study guide provides a complete walkthrough for implementing a custom Nagios plugin in a Docker environment on Windows. The plugin demonstrates fundamental concepts of Nagios monitoring including thresholds, exit codes, and service definitions.

Key takeaways:
- Custom plugins extend Nagios functionality
- Proper permissions and paths are crucial
- Configuration syntax must be precise
- Testing at each step prevents issues
- Regular monitoring ensures continued effectiveness

Continue exploring Nagios documentation and consider creating additional custom plugins for comprehensive system monitoring.
