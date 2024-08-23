# Simple MySQL Backup Automation: Complete Guide

This guide provides a straightforward approach to setting up a MySQL server in Docker, creating a dummy database, and using a Python script to back it up on Windows 11.

## 1. Prerequisites

- Windows 11 PC
- Docker Desktop installed and running
- Python 3.x installed

## 2. Setup MySQL in Docker

1. Open Command Prompt and run:
   ```
   docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d mysql:latest
   ```
   This creates a MySQL container with root password set to 'root'.

2. Connect to the MySQL container:
   ```
   docker exec -it mysql-container mysql -uroot -proot
   ```

3. Create a dummy database and table:
   ```sql
   CREATE DATABASE dummy_db;
   USE dummy_db;
   CREATE TABLE dummy_table (id INT, name VARCHAR(50));
   INSERT INTO dummy_table VALUES (1, 'John'), (2, 'Jane');
   EXIT;
   ```

## 3. Python Backup Script

Save the following script as `mysql_backup.py`:

```python
import subprocess
from datetime import datetime

def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"dummy_db_backup_{timestamp}.sql"

    mysqldump_cmd = [
        "docker", "exec", "mysql-container",
        "mysqldump",
        "-uroot", "-proot",
        "dummy_db"
    ]

    try:
        with open(backup_file, 'w') as f:
            subprocess.run(mysqldump_cmd, stdout=f, check=True)
        print(f"Backup created successfully: {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")

if __name__ == "__main__":
    create_backup()
```

## 4. Usage

1. Open Command Prompt in the directory containing `mysql_backup.py`

2. Run the script:
   ```
   python mysql_backup.py
   ```

3. The script will create a backup file named `dummy_db_backup_YYYYMMDD_HHMMSS.sql` in the same directory.

## 5. Troubleshooting

- If Docker isn't running, start Docker Desktop and wait for it to initialize.
- If the MySQL container isn't running, start it with:
  ```
  docker start mysql-container
  ```
- If you get a "command not found" error, ensure Python is in your system PATH.

Remember, this setup uses root credentials for simplicity. For real-world applications, always use strong, unique passwords and proper security measures.
