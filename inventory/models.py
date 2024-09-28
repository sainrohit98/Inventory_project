from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)  
    description = models.TextField()
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name', 'description'] 