# DevSecOps Flask Application Guide

This guide demonstrates basic DevSecOps practices in a Python Flask application. We'll create two main files: `app.py` for our Flask application and a GitHub Actions workflow file for continuous integration with security checks.

## Creating the Project on GitHub

1. Log in to your GitHub account.
2. Click the '+' icon in the top right corner and select 'New repository'.
3. Name your repository (e.g., "devsecops-flask-demo").
4. Choose 'Public' for visibility.
5. Initialize the repository with a README.
6. Click 'Create repository'.

## Creating app.py

In your new repository, create a new file named `app.py`:

1. Click 'Add file' > 'Create new file'.
2. Name the file `app.py`.
3. Copy and paste the following code:

```python
from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Flask App</title>
</head>
<body>
    <h1>Welcome to Secure Flask App</h1>
    <form method="POST">
        <input type="text" name="user_input" placeholder="Enter your name">
        <input type="submit" value="Submit">
    </form>
    {% if name %}
    <h2>Hello, {{ name }}!</h2>
    {% endif %}
</body>
</html>
"""

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/', methods=['GET', 'POST'])
def hello():
    name = None
    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        if re.match("^[A-Za-z0-9 ]+$", user_input):
            name = user_input
        else:
            name = "Invalid input"
    return render_template_string(HTML_TEMPLATE, name=name)

if __name__ == '__main__':
    app.run(debug=True)
```

4. Commit the new file.

### Explanation of app.py

1. **Security Headers**: 
   The `add_security_headers` function adds three security headers to every response:
   - `X-Content-Type-Options: nosniff`: Prevents MIME type sniffing.
   - `X-Frame-Options: SAMEORIGIN`: Protects against clickjacking attacks.
   - `X-XSS-Protection: 1; mode=block`: Enables the browser's built-in XSS protection.

2. **Input Validation**:
   In the `hello` function, we use a regular expression `^[A-Za-z0-9 ]+$` to validate user input. This ensures only alphanumeric characters and spaces are accepted, helping to prevent injection attacks.

3. **Template Injection Prevention**:
   While we use `render_template_string` for simplicity, in a production environment, it's recommended to use `render_template` with separate template files to further mitigate template injection risks.

4. **Debug Mode**:
   Note that `debug=True` is set for development purposes. In a production environment, this should be set to `False`.

## Creating the GitHub Actions Workflow

Next, we'll create a GitHub Actions workflow for continuous integration with security checks:

1. In your repository, click 'Add file' > 'Create new file'.
2. Name the file `.github/workflows/ci.yml` (this will automatically create the necessary directories).
3. Copy and paste the following YAML content:

```yaml
name: CI
on: [push]
jobs:
  security-checks:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        pip install safety bandit flask
    - name: Run safety check
      run: safety check
    - name: Run bandit
      run: bandit -r . -f custom
```

4. Commit the new file.

### Explanation of ci.yml

This GitHub Actions workflow does the following:

1. **Trigger**: The workflow runs on every push to the repository.

2. **Environment**: It uses an Ubuntu latest runner.

3. **Steps**:
   - Checks out the repository code.
   - Sets up Python 3.x.
   - Installs necessary dependencies, including:
     - `safety`: For checking Python dependencies for known vulnerabilities.
     - `bandit`: A tool designed to find common security issues in Python code.
     - `flask`: Our web framework.
   - Runs `safety check` to scan dependencies for known security issues.
   - Runs `bandit` to perform a static code analysis for common security issues.

This CI pipeline helps to automatically catch potential security vulnerabilities both in our code and our dependencies every time we push changes to the repository.

## Conclusion

By implementing these files, we've created a basic Flask application with some key DevSecOps practices:

1. Security headers to protect against common web vulnerabilities.
2. Input validation to prevent injection attacks.
3. A CI pipeline that automatically checks for security issues in both our code and dependencies.

Remember, this is just a starting point. In a real-world application, you would want to implement additional security measures such as:

- Proper authentication and authorization
- HTTPS enforcement
- More comprehensive input validation and sanitization
- Secure session management
- Regular dependency updates
- Comprehensive error handling and logging

Always stay updated on the latest security best practices and continuously improve your security posture.
