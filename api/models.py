from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

#create the custom user model
class User(AbstractUser):
    pass 

#create the product model 
class Product(models.Model):
    name= models.CharField(max_length=200)
    description= models.TextField()
    price= models.DecimalField(max_digits=6, decimal_places=2)
    stock= models.PositiveIntegerField()
    image= models.ImageField(upload_to='products', blank=True, null= True)


    @property
    def in_stock(self):
        return self.stock > 0
    

    def __str__(self):
        return self.name

#create the order model 
class Order(models.Model):
    class StatusChoice(models.TextChoices):
        PENDING= 'pending'
        CONFIRMED= 'confirmed'
        CANCELED= 'canceled'
    order_id= models.UUIDField(primary_key=True, default=uuid.uuid4)
    user= models.ForeignKey('User', on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=200, choices=StatusChoice.choices, default=StatusChoice.PENDING)
    products= models.ManyToManyField('Product', through='OrderItem', related_name='orders')

    def __str__(self):
        return f'Order {self.order_id} By {self.user.username}'

#create the order item model 
class OrderItem(models.Model):
    order= models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product= models.ForeignKey(Product, on_delete= models.CASCADE)
    quantity= models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Order {self.order.order_id}'