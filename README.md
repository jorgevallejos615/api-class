# Inventory API Client

## Installation
```bash
cp api_client.py src/
```

## Running Tests
```bash
pytest tests/
```

## Usage
```python
from src.api_client import InventoryAPIClient

api_client = InventoryAPIClient()
inventory = api_client.get_inventory()
print(inventory)
```