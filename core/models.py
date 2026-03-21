from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# 1. Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

# 2. Product Model
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField()
    # We are using image_url because it's simpler and works with your current templates
    image_url = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.name
    

# 3. Sale Model (This is the new feature!)
class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} sold by {self.sold_by.username}"
    
    
    
 #4  EXPENSE MODEL 
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Rent', 'Shop Rent'),
        ('Salary', 'Staff Salary'),
        ('Bills', 'Electricity/Water Bills'),
        ('Maintenance', 'Repairs & Maintenance'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=100) # e.g., "January Rent"
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    date_added = models.DateField(default=timezone.now)
    
    # We track who added the expense
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
    
#5 customer models
class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
#6 staff salary 
class Staff(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50, default='Salesperson') 
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_hired = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
#7 supplier 
class Supplier(models.Model):
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
    
    
#8 invoice and invoice items
class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):

        name = self.customer.name if self.customer else "Walk-in Customer"
        return f"Invoice #{self.id} - {name}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) 

    def get_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"