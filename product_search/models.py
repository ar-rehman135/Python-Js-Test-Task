
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    selected = models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        return self.name


class SelectedProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="selected_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="selected_by_users")

    class Meta:
        unique_together = ("user", "product") 
    def __str__(self):
        return f"{self.user.username} selected {self.product.name}"