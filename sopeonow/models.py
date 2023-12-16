import random
import string
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    iin = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    quantity_sold = models.PositiveIntegerField(default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_profit(self):
        return (self.selling_price - self.cost) * self.quantity_sold

    def calculate_revenue(self):
        return self.selling_price * self.quantity_sold
    
    def generate_unique_iin(self):
        while True:
            iin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if not Inventory.objects.filter(iin=iin).exists():
                return iin
    # class Meta:
    #     app_label='Inventory'

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Inventory)
def generate_and_set_iin(sender, instance, **kwargs):
    if not instance.iin:
        instance.iin = instance.generate_unique_iin()
        
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    orderdttm = models.DateTimeField()
    is_received = models.BooleanField(default=False)
    is_cancel = models.BooleanField(default=False)
    # class Meta:
    #     app_label='Order'
    def __str__(self):
        return f"{self.name}'s order for {self.item.name}"

class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    item = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    transactiondttm = models.DateTimeField()
    # class Meta:
    #     app_label='Transaction'
    def __str__(self):
        return f"Transaction for {self.quantity} {self.item.name}(s) by {self.name}"

