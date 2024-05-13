from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, InventoryItem

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	profile_photo = forms.ImageField(required=False)
	address = forms.CharField(required=False)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2', 'profile_photo', 'address']
		help_texts={'username':''}



class InventoryItemForm(forms.ModelForm):
	category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
	class Meta:
		model = InventoryItem
		fields = ['name', 'quantity', 'category','image','unit_price','user']

class QuantityUpdateForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

class QuantityIssueForm(forms.Form):
    quantity = forms.IntegerField(min_value=1) 

class BillForm(forms.Form):
    customer_name = forms.CharField(max_length=100)

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email')
    
class OTPValidationForm(forms.Form):
    otp = forms.CharField(label='OTP', max_length=6)
    
class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
	# forms.py



class InventorySearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100, required=False)
    category = forms.CharField(label='Category', max_length=100, required=False)
    # Add more fields for additional filtering criteria (e.g., quantity)



class SellItemForm(forms.Form):
    quantity = forms.IntegerField(label='Quantity to Sell', min_value=1)


# forms.py


class SaleForm(forms.Form):
    quantity = forms.IntegerField(label='Quantity')
    unit_price = forms.DecimalField(label='Unit Price', widget=forms.TextInput(attrs={'readonly': True}))




# forms.py

from django import forms
from .models import InventoryItem

class SalesForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    mobile_number = forms.CharField(max_length=15)
    address = forms.CharField(max_length=255)
    items = forms.ChoiceField(choices=[])  # Dynamic choices for items

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['items'].choices = [(item.id, item.name) for item in InventoryItem.objects.all()]


from django import forms
from .models import InventoryItem

class SellItemForm(forms.Form):
    item = forms.ModelChoiceField(queryset=None)
    quantity = forms.IntegerField()
    unit_price = forms.FloatField()
    sale_date = forms.DateField()
    customer_name = forms.CharField()
    mobile_number = forms.CharField()

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['item'].queryset = InventoryItem.objects.filter(user=user)





# forms.py
from django import forms
from .models import InventoryItem

class SellMultipleItemsForm(forms.Form):
    items = forms.ModelMultipleChoiceField(queryset=InventoryItem.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    customer_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Retrieve the user from kwargs
        super().__init__(*args, **kwargs)
        # Filter items based on the user's inventory
        if self.user:
            self.fields['items'].queryset = InventoryItem.objects.filter(user=self.user)

    def clean(self):
        cleaned_data = super().clean()
        items = cleaned_data.get('items')
        quantity = cleaned_data.get('quantity')

        if items and quantity:
            for item in items:
                if quantity > item.quantity:
                    raise forms.ValidationError(f"Quantity for '{item.name}' exceeds available stock.")
        return cleaned_data

    def save(self):
        # Perform any additional processing or saving if needed
        pass




# forms.py
# forms.py

from django import forms
from decimal import Decimal
from .models import BoughtItem

class BuyItemForm(forms.ModelForm):
    bought_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = BoughtItem
        fields = ['supplier', 'bought_date', 'product_name', 'quantity', 'unit_price']

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        unit_price = cleaned_data.get('unit_price')

        if quantity is not None and unit_price is not None:
            total_price = Decimal(quantity) * unit_price
            gst_price = total_price * Decimal('0.18')  # Assuming 18% GST

            cleaned_data['total_price'] = total_price
            cleaned_data['gst_price'] = gst_price
            
            # Calculate total price including GST
            total_price_gst = total_price + gst_price
            cleaned_data['total_price_gst'] = total_price_gst  # Include total_price_gst in cleaned data

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.total_price = self.cleaned_data.get('total_price')
        instance.gst_price = self.cleaned_data.get('gst_price')
        instance.total_price_gst = self.cleaned_data.get('total_price_gst')  # Assign total_price_gst from cleaned data
        if commit:
            instance.save()
        return instance
