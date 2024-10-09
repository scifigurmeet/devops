# Linux Shell Scripting Guide for Beginners

## 1. Introduction to Linux and the Shell

Linux is an open-source operating system that provides a powerful command-line interface called the shell. The shell allows users to interact with the system, execute commands, and automate tasks through scripts.

Popular Linux shells include:
- Bash (Bourne Again Shell) - The most common shell in Linux
- Zsh (Z Shell) - An extended version of Bash with additional features
- Fish (Friendly Interactive Shell) - A user-friendly shell with auto-suggestions

This guide will focus on Bash, as it's the most widely used shell in Linux distributions.

## 2. Basic Shell Commands

Let's start with some essential commands:

- `ls`: List files and directories
- `cd`: Change directory
- `pwd`: Print working directory
- `mkdir`: Create a new directory
- `touch`: Create a new file or update timestamps
- `cp`: Copy files or directories
- `mv`: Move or rename files or directories
- `rm`: Remove files or directories
- `cat`: Display file contents
- `echo`: Print text to the terminal
- `man`: Display manual pages for commands

Example usage:
```bash
ls -l
cd Documents
pwd
mkdir NewFolder
touch newfile.txt
cp newfile.txt NewFolder/
mv newfile.txt renamed_file.txt
rm renamed_file.txt
cat example.txt
echo "Hello, World!"
man ls
```

## 3. File System Navigation

Understanding the Linux file system is crucial:

- `/`: Root directory
- `/home`: User home directories
- `/etc`: System configuration files
- `/var`: Variable data (logs, temporary files)
- `/bin`, `/usr/bin`: Essential user command binaries
- `/sbin`, `/usr/sbin`: System administration command binaries

Navigation commands:
- `cd /`: Go to root directory
- `cd ~` or `cd`: Go to home directory
- `cd ..`: Go up one directory
- `cd -`: Go to previous directory

## 4. Text Manipulation

Text manipulation is a powerful feature in Linux:

- `grep`: Search for patterns in text
- `sed`: Stream editor for filtering and transforming text
- `awk`: Text processing tool for data extraction and reporting
- `sort`: Sort lines of text
- `uniq`: Report or omit repeated lines
- `wc`: Word, line, character, and byte count

Example usage:
```bash
grep "error" log.txt
sed 's/old/new/g' file.txt
awk '{print $1}' data.txt
sort numbers.txt
sort numbers.txt | uniq
wc -l file.txt
```

## 5. Shell Scripting Basics

Shell scripts are text files containing a series of commands. To create a shell script:

1. Create a file with a `.sh` extension (e.g., `myscript.sh`)
2. Add the shebang line at the top: `#!/bin/bash`
3. Add your commands
4. Make the script executable: `chmod +x myscript.sh`
5. Run the script: `./myscript.sh`

Example script:
```bash
#!/bin/bash
echo "Hello, World!"
current_date=$(date)
echo "Current date and time: $current_date"
```

## 6. Variables and Data Types

Variables in shell scripts:

- Assignment: `variable_name=value`
- Access: `$variable_name`
- Command substitution: `result=$(command)`

Example:
```bash
name="John"
echo "Hello, $name!"

current_dir=$(pwd)
echo "Current directory: $current_dir"
```

## 7. Control Structures

Control structures help manage the flow of your scripts:

1. Conditionals:
```bash
if [ condition ]; then
    # commands
elif [ condition ]; then
    # commands
else
    # commands
fi
```

2. Loops:
```bash
# For loop
for item in list; do
    # commands
done

# While loop
while [ condition ]; do
    # commands
done
```

Example:
```bash
#!/bin/bash
for i in {1..5}; do
    echo "Number: $i"
done

count=0
while [ $count -lt 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done
```

## 8. Functions

Functions allow you to organize and reuse code:

```bash
function_name() {
    # commands
}

# Call the function
function_name
```

Example:
```bash
#!/bin/bash
greet() {
    echo "Hello, $1!"
}

greet "Alice"
greet "Bob"
```

## 9. Input/Output Operations

Handling input and output in shell scripts:

- Read user input: `read variable_name`
- Redirect output: `command > file.txt`
- Append output: `command >> file.txt`
- Redirect input: `command < file.txt`
- Pipe commands: `command1 | command2`

Example:
```bash
#!/bin/bash
echo "Enter your name:"
read name
echo "Hello, $name!" > greeting.txt
cat greeting.txt
```

## 10. Advanced Topics

As you progress, explore these advanced topics:

- Regular expressions
- Process management
- File descriptors and redirection
- Subshells
- Error handling and debugging
- Command-line arguments
- Array manipulation

## 11. Best Practices and Tips

- Comment your code for clarity
- Use meaningful variable names
- Handle errors and edge cases
- Use shellcheck for script validation
- Keep scripts modular and reusable
- Use version control (e.g., Git) for your scripts

## 12. Resources for Further Learning

- Bash Manual
- Linux Documentation Project
- ShellCheck - Online shell script analyzer
- Explainshell - Explain shell commands
- Online platforms: Codecademy, Linux Academy, edX

Remember, practice is key to mastering shell scripting. Start with small scripts and gradually build more complex ones as you become comfortable with the concepts.
