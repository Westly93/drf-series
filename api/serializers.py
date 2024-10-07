from rest_framework import serializers
from .models import User, Order, OrderItem, Product


#product serializer 
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields= (
            'id',
            'name',
            'description',
            'price', 
            'stock'
        )

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("The price can not be less than or eqaul to 0.")
        return value
    
#order item serializer 
class OrderItemSerializer(serializers.ModelSerializer):
    #product= ProductSerializer(read_only= True)
    product_name= serializers.CharField(source= 'product.name')
    product_price= serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        source= 'product.price'
    )
    class Meta:
        model= OrderItem
        fields= (
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal',
        )   

#serializing order model
class OrderSerializer(serializers.ModelSerializer):
    items= OrderItemSerializer(many= True, read_only= True)
    total_price= serializers.SerializerMethodField()

    def get_total_price(self, obj):
        order_items= obj.items.all()
        return sum(item.item_subtotal for item in order_items)
    
    class Meta:
        model= Order
        fields= (
            'order_id',
            'user', 
            'created_at',
            'status',
            'items',
            'total_price',
        )

