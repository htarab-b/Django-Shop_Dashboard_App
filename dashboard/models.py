from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Shops(models.Model):
    shop_name = models.CharField(verbose_name='Shop Name', max_length=20)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    order_count = models.IntegerField(verbose_name='Order Count', default=0)
    delivered_count = models.IntegerField(verbose_name='Number of orders delivered', default=0)
    pending_count = models.IntegerField(verbose_name='Number of pending delivery orders', default=0)
    def __str__(self):
        return self.shop_name

class Orders(models.Model):
    status_choices = (
        ('Delivery Pending', 'Delivery pending'),
        ('Order Delivered', 'Order delivered')
    )
    shop = models.ForeignKey(to=Shops, on_delete=models.CASCADE)
    customer = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True)
    customer_name = models.CharField(verbose_name='Customer Name', max_length=20, null=True)
    status = models.CharField(choices=status_choices, default='Delivery Pending', max_length=16)
