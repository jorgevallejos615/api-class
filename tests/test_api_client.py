from api_client import InventoryAPIClient
import pytest

@pytest.fixture
def api_client():
    return InventoryAPIClient()

def test_get_inventory(api_client):
    inventory = api_client.get_inventory()
    assert isinstance(inventory, list)
    assert len(inventory) > 0

def test_add_item(api_client):
    new_item = {
        'title': 'New Item',
        'description': 'This is a new item',
        'price': 100,
        'stock': 10
    }
    added_item = api_client.add_item(new_item)
    assert added_item['title'] == new_item['title']

def test_update_item(api_client):
    item_id = api_client.get_inventory()[0]['id']
    updated_item = {
        'title': 'Updated Item',
        'description': 'This is an updated item',
        'price': 200,
        'stock': 20
    }
    updated_item_response = api_client.update_item(item_id, updated_item)
    assert updated_item_response['title'] == updated_item['title']

def test_delete_item(api_client):
    item_id = api_client.get_inventory()[0]['id']
    deleted_item = api_client.delete_item(item_id)
    assert deleted_item['id'] == item_id
