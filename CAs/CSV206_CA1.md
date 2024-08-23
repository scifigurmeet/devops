# Practical Assignment: Scripting and Automation

## Duration: 15-20 minutes

### Objective
This assignment will test your understanding of conditional statements, loops, and file management automation using Python. You'll create a script that manages files based on their age and performs database backups.

### Prerequisites
- Basic knowledge of Python
- Python 3.x installed on your system
- Access to a MySQL database (local or remote)
- `mysql-connector-python` library installed (`pip install mysql-connector-python`)

### Task 1: File Management Automation (10 minutes)

Create a Python script that does the following:

1. Scans a specified directory for files with the extension ".archive"
2. Checks the last modification date of each ".archive" file
3. Deletes any ".archive" files that are older than two days

#### Requirements:
- Use conditional statements to check file extensions and ages
- Use a loop to iterate through the files in the directory
- Use the `os` and `datetime` modules for file operations and date calculations

#### Starter Code:
```python
import os
import datetime

def clean_old_archives(directory):
    # Your code here
    pass

# Test your function
clean_old_archives("/path/to/your/directory")
```

### Task 2: Database Backup Automation (10 minutes)

Extend your script to include a function that:

1. Connects to a MySQL database
2. Creates a backup of the specified database
3. Saves the backup file with a timestamp in its name
4. Moves the backup file to a designated backup directory

#### Requirements:
- Use the `mysql-connector-python` library for database operations
- Use string formatting to create unique filenames with timestamps
- Use the `shutil` module to move files

#### Starter Code:
```python
import mysql.connector
import datetime
import shutil

def backup_mysql_db(host, user, password, database, backup_dir):
    # Your code here
    pass

# Test your function
backup_mysql_db("localhost", "your_username", "your_password", "your_database", "/path/to/backup/directory")
```

### Bonus Challenge (if time permits):
Combine both functions into a single script that:
1. Performs the archive cleanup
2. Checks if 12 hours have passed since the last backup
3. If so, performs a new database backup

### Submission Guidelines:
1. Submit your Python script(s) with clear comments explaining your code.
2. Include a brief explanation (2-3 sentences) of how you would schedule this script to run automatically on a regular basis.

### Evaluation Criteria:
- Correct implementation of file management logic
- Proper use of conditional statements and loops
- Successful database backup functionality
- Code readability and comments
- Bonus points for completing the challenge and explaining scheduling

Good luck!
