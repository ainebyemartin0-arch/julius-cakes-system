from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Order(models.Model):
    DELIVERY_OPTIONS = [('pickup', 'Pickup'), ('delivery', 'Delivery')]
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('baking', 'Baking in Progress'),
        ('ready', 'Ready for Pickup/Delivery'),
        ('completed', 'Completed'),
    ]

    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=15)
    customer_email = models.EmailField(blank=True, null=True)
    delivery_option = models.CharField(max_length=10, choices=DELIVERY_OPTIONS, default='pickup')
    delivery_address = models.TextField(blank=True, null=True)
    required_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New fields for custom orders
    cake_details = models.TextField(blank=True, null=True)
    reference_image = models.ImageField(upload_to='custom_cakes/', blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    custom_message = models.CharField(max_length=200, blank=True, null=True)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
