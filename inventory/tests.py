import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, force_authenticate
from unittest.mock import patch
from .models import InventoryItem
from .serializers import InventoryItemSerializer

class InventoryItemModelTest(TestCase):
    def test_create_inventory_item(self):
        item = InventoryItem.objects.create(
            name="Test Item",
            description="This is a test item",
            quantity=10
        )
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.description, "This is a test item")
        self.assertEqual(item.quantity, 10)

    def test_unique_together_constraint(self):
        InventoryItem.objects.create(
            name="Test Item",
            description="This is a test item",
            quantity=10
        )
        with self.assertRaises(Exception):
            InventoryItem.objects.create(
                name="Test Item",
                description="This is a test item",
                quantity=5
            )

class InventoryItemViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.item_data = {
            "name": "Test Item",
            "description": "This is a test item",
            "quantity": 10
        }
        self.url = reverse('inventoryitem-list')

    @patch('inventory.views.cache_item')
    def test_create_inventory_item(self, mock_cache_item):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InventoryItem.objects.count(), 1)
        self.assertEqual(InventoryItem.objects.get().name, 'Test Item')
        mock_cache_item.assert_called_once()

    @patch('inventory.views.get_cached_item')
    @patch('inventory.views.cache_item')
    def test_get_inventory_item(self, mock_cache_item, mock_get_cached_item):
        item = InventoryItem.objects.create(**self.item_data)
        mock_get_cached_item.return_value = None
        url = reverse('inventoryitem-detail', kwargs={'pk': item.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item_data['name'])
        mock_cache_item.assert_called_once()

    @patch('inventory.views.cache_item')
    def test_update_inventory_item(self, mock_cache_item):
        item = InventoryItem.objects.create(**self.item_data)
        url = reverse('inventoryitem-detail', kwargs={'pk': item.pk})
        updated_data = {
            "name": "Updated Test Item",
            "description": "This is an updated test item",
            "quantity": 15
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(InventoryItem.objects.get().name, 'Updated Test Item')
        
        # Check that cache_item was called twice
        self.assertEqual(mock_cache_item.call_count, 2)
        
        # Check the content of the calls
        calls = mock_cache_item.call_args_list
        self.assertEqual(len(calls), 2)
        
        # First call should be with the original data (when getting the object)
        self.assertEqual(calls[0][0][0], item.id)
        self.assertEqual(calls[0][0][1]['name'], 'Test Item')
        
        # Second call should be with the updated data
        self.assertEqual(calls[1][0][0], item.id)
        self.assertEqual(calls[1][0][1]['name'], 'Updated Test Item')

    @patch('inventory.views.delete_cached_item')
    def test_delete_inventory_item(self, mock_delete_cached_item):
        item = InventoryItem.objects.create(**self.item_data)
        url = reverse('inventoryitem-detail', kwargs={'pk': item.pk})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InventoryItem.objects.count(), 0)
        mock_delete_cached_item.assert_called_once_with(item.id)

