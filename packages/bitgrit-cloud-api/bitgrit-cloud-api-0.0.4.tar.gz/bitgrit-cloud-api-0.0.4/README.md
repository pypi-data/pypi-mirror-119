# bitgrit-cloud-api
Library to interact with our cloud service(GCP)

> Note: look inside `./dist/` folder to see the latest build `.whl` file.

# How to setup the Library:
### Install Dependencies/Packages:

### Run this command:
```bash
pip install -r requirements.txt
```

### Import the Library:
```python
from dsn.bitgrit.gcp.dataset_api import DatasetAPI
```

### To checkout documentation:
```bash
pydoc dataset
```

### To set the environment variable
```bash
export VAULT_TOKEN=<vault-token>
export VAULT_URL=<vault-url>
```

### To run the test
```bash
python -m unittest
```
### To package the library
```bash
python -m pip install --user --upgrade setuptools wheel
python setup.py sdist bdist_wheel
```