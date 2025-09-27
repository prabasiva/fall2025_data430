# Python Virtual Environment and Faker Installation Guide

## Step 1: Create Python Virtual Environment

### Using venv (built-in)
```bash
# Create virtual environment
python3 -m venv myenv

# Activate virtual environment
# On macOS/Linux:
source myenv/bin/activate

# On Windows:
myenv\Scripts\activate
```

### Verify virtual environment is active
```bash
which python
# Should show path to your virtual environment
```

## Step 2: Install Faker Library

### Install faker in virtual environment
```bash
# Make sure virtual environment is activated
pip install faker
```

### Verify installation
```bash
pip list | grep faker
```

## Step 3: Usage Example

### Create test script
```python
from faker import Faker

# Create Faker instance
fake = Faker()

# Generate fake data
print(f"Name: {fake.name()}")
print(f"Email: {fake.email()}")
print(f"Address: {fake.address()}")
print(f"Phone: {fake.phone_number()}")
print(f"Company: {fake.company()}")
```

### Run the script
```bash
python test_faker.py
```

## Step 4: Deactivate Virtual Environment

```bash
deactivate
```

## Common Commands Summary

```bash
# Create venv
python3 -m venv myenv

# Activate
source myenv/bin/activate

# Install faker
pip install faker

# Deactivate
deactivate
```