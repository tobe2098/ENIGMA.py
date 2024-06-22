Using YAML (Yet Another Markup Language) to store and retrieve configuration data for a module is a common and efficient practice. YAML is human-readable and easy to edit, making it ideal for configuration files. Below are the steps to store and retrieve configuration data using YAML in Python:

### 1. Install PyYAML

First, you need to install the `PyYAML` library if you haven't already. You can install it using pip:

```bash
pip install pyyaml
```

### 2. Create a YAML Configuration File

Create a YAML file (e.g., `config.yaml`) to store your configuration. Here’s an example:

```yaml
# config.yaml
database:
  host: localhost
  port: 3306
  username: user
  password: pass

server:
  host: 0.0.0.0
  port: 8000

logging:
  level: DEBUG
  file: /var/log/myapp.log
```

### 3. Load Configuration Data in Python

In your Python script, you can load this configuration using `PyYAML`. Here’s an example of how to do it:

```python
import yaml

# Function to load the YAML configuration file
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Load the configuration
config = load_config('config.yaml')

# Access the configuration data
database_host = config['database']['host']
database_port = config['database']['port']
server_host = config['server']['host']
server_port = config['server']['port']
logging_level = config['logging']['level']

print(f"Database Host: {database_host}")
print(f"Database Port: {database_port}")
print(f"Server Host: {server_host}")
print(f"Server Port: {server_port}")
print(f"Logging Level: {logging_level}")
```

### 4. Save Configuration Data to YAML

If you need to update the configuration and save it back to a YAML file, you can do so like this:

```python
import yaml

# Function to save the YAML configuration file
def save_config(file_path, config):
    with open(file_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

# Update the configuration
config['database']['host'] = '127.0.0.1'
config['database']['port'] = 5432

# Save the updated configuration
save_config('config.yaml', config)
```

### Full Example

Here’s a complete example that combines loading, modifying, and saving the configuration:

```python
import yaml

# Function to load the YAML configuration file
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Function to save the YAML configuration file
def save_config(file_path, config):
    with open(file_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

# Load the configuration
config = load_config('config.yaml')

# Access the configuration data
database_host = config['database']['host']
database_port = config['database']['port']
server_host = config['server']['host']
server_port = config['server']['port']
logging_level = config['logging']['level']

print(f"Database Host: {database_host}")
print(f"Database Port: {database_port}")
print(f"Server Host: {server_host}")
print(f"Server Port: {server_port}")
print(f"Logging Level: {logging_level}")

# Update the configuration
config['database']['host'] = '127.0.0.1'
config['database']['port'] = 5432

# Save the updated configuration
save_config('config.yaml', config)
```

This example demonstrates how to read a configuration from a YAML file, modify the configuration in your Python code, and save the updated configuration back to the YAML file.