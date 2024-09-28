from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import InventoryItem
from .serializers import InventoryItemSerializer
from .redis_utils import cache_item, get_cached_item, delete_cached_item
import logging

logger = logging.getLogger(__name__)

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        cached_item = get_cached_item(obj.id)
        if not cached_item:
            serializer = self.get_serializer(obj)
            cache_item(obj.id, serializer.data)
            logger.info(f"Caching item {obj.id}")
        else:
            logger.info(f"Retrieved item {obj.id} from cache")
        return obj  # Always return the actual object, not cached data

    def create(self, request, *args, **kwargs):
        logger.info("Received request to create a new inventory item")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                logger.info("Validation successful, creating item")
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                logger.info(f"Item created successfully with ID: {serializer.data.get('id')}")
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            except serializers.ValidationError as e:
                logger.error(f"Validation failed during creation: {e.detail}")
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        logger.error(f"Invalid data for creation: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        logger.info(f"Received request to {'partially' if partial else 'fully'} update item with ID: {kwargs.get('pk')}")
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            try:
                logger.info(f"Validation successful for update on item with ID: {instance.id}")
                self.perform_update(serializer)
                logger.info(f"Item updated successfully with ID: {instance.id}")
                return Response(serializer.data)
            except serializers.ValidationError as e:
                logger.error(f"Validation failed during update: {e.detail}")
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        logger.error(f"Invalid data for update on item with ID: {instance.id}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        logger.info(f"Performing creation for new item: {serializer.validated_data.get('name')}")
        instance = serializer.save()
        cache_item(instance.id, serializer.data)
        logger.info(f"Item with ID {instance.id} cached after creation")

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(f"Performing update for item: {instance.id}")
        cache_item(instance.id, serializer.data)
        logger.info(f"Item with ID {instance.id} cached after update")

    def perform_destroy(self, instance):
        logger.info(f"Performing deletion for item: {instance.id}")
        delete_cached_item(instance.id)
        logger.info(f"Item with ID {instance.id} removed from cache")
        instance.delete()
        logger.info(f"Item with ID {instance.id} deleted from the database")

