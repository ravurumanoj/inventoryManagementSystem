
from django import forms
from .models import Inventory

class SellItemForm(forms.Form):
    quantity = forms.IntegerField(label='Quantity')
    selling_price = forms.DecimalField(label='Selling Price')

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than zero.')
        return quantity

    def clean_selling_price(self):
        selling_price = self.cleaned_data['selling_price']
        if selling_price <= 0:
            raise forms.ValidationError('Selling price must be greater than zero.')
        return selling_price

class CreateItemForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['name', 'cost', 'quantity', 'selling_price']
