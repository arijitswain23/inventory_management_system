from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photo/', blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
	
    def __str__(self):
        return self.user.username
    

class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Add the unit_price field
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(upload_to='inventory_images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    def delete(self, *args, **kwargs):
        # Before deleting the item, you may want to perform any additional cleanup actions
        
        # Call the delete method of the parent class to remove the item from the database
        super().delete(*args, **kwargs)
    


class SalesTransaction(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateField()
    customer_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.customer_name} - {self.sale_date}"
    
    



    

class Category(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name
	


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    valid_until = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Ensure user_id is populated before saving
        if not self.user_id:
            raise ValueError("user_id must be provided")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email


class QuantityAdjustment(models.Model):
    item = models.ForeignKey(InventoryItem, related_name='quantity_adjustments', on_delete=models.CASCADE)
    quantity_added = models.IntegerField()
    quantity_removed = models.IntegerField()
    # Other fields as needed

    def units_sold(self):
        # Calculate the total units sold for this item
        return self.salestransaction_set.aggregate(total_units_sold=models.Sum('quantity_sold'))['total_units_sold'] or 0

    def units_added(self):
        # Calculate the total units added for this item
        # You need to define how units are added, possibly through another related model
        return 0  # Replace this with your logic for calculating units added
    
class SalesItem(models.Model):
    sales_transaction = models.ForeignKey(SalesTransaction, on_delete=models.CASCADE)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity_sold = models.IntegerField()


from django.db import models

class SalesRecord(models.Model):
    customer_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=20)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class SalesRecordItem(models.Model):
    sales_record = models.ForeignKey(SalesRecord, related_name='items', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)


class BuyTransaction(models.Model):
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    supplier_name = models.CharField(max_length=100)
    supplier_contact = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.supplier_name} - {self.purchase_date}"



# models.py

from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class BoughtItem(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    gst_price = models.DecimalField(max_digits=10, decimal_places=2)
    bought_date = models.DateField()
    total_price_gst = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Add this line

    def save(self, *args, **kwargs):
        if self.total_price is not None and self.gst_price is not None:
            self.total_price_gst = self.total_price + self.gst_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name



