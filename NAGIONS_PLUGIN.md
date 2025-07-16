✅ Plugin Code: `check_disk_simple.sh`
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


/opt/Custom-Nagios-Plugins/`check_disk_simple.sh`


define command {
    command_name    check_disk_simple
    command_line    /opt/Custom-Nagios-Plugins/check_disk_simple.sh
}

define service {
    use                 generic-service
    host_name           localhost
    service_description Root Disk Simple Check
    check_command       check_disk_simple
}
chmod +x check_disk_simple.sh

Crearte a markdown study guide to perform this custom plugin practical.

Add step by step. nagios is running inside nagios docker container. Windows CMD.
