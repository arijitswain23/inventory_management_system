from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm,QuantityUpdateForm,QuantityIssueForm,BillForm,ForgotPasswordForm,SetNewPasswordForm
from .models import InventoryItem, Category, UserProfile,SalesTransaction
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from .models import UserProfile

class ProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'inventory/profile.html'

    def get_object(self):
        return self.request.user.userprofile

	
class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'inventory/register.html'

    def form_valid(self, form):
        user = form.save()
        profile = UserProfile(user=user, profile_photo=self.request.FILES['profile_photo'], address=form.cleaned_data['address'])
        profile.save()
        return redirect('login')
	
class Index(TemplateView):
	template_name = 'inventory/index.html'


class SaleSummary1View(TemplateView):
     template_name='inventory/sale_summary1.html'
     
class Thanku(TemplateView):
	template_name = 'inventory/thanku.html'



from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from django.shortcuts import render
from .models import InventoryItem, Category
from .forms import InventoryItemForm

class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # Check if the user creating the item is a superuser
        if self.request.user.is_superuser:
            # Fetch the user instance corresponding to the provided username
            user_instance = User.objects.get(username=form.cleaned_data['user'])
            # Set the user instance as the user for the InventoryItem instance
            form.instance.user = user_instance
        else:
            # For non-superusers, set the logged-in user as the user for the InventoryItem instance
            form.instance.user = self.request.user
        return super().form_valid(form)
    
    
    
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from .models import InventoryItem, BuyTransaction
from .forms import BuyItemForm, InventoryItemForm


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        # Fetch inventory items
        items = InventoryItem.objects.filter(user=request.user).order_by('quantity')

        # Fetch low inventory items
        low_inventory = items.filter(quantity__lte=LOW_QUANTITY)

        # Fetch buy items
        buy_items = BuyTransaction.objects.filter(user=request.user)

        # Display message for low inventory items
        if low_inventory.exists():
            if low_inventory.count() > 1:
                messages.error(request, f'{low_inventory.count()} items have low inventory')
            else:
                messages.error(request, f'{low_inventory.count()} item has low inventory')

        # Get IDs of low inventory items
        low_inventory_ids = low_inventory.values_list('id', flat=True)

        # Initialize forms for adding inventory items and buying items
        add_item_form = InventoryItemForm()
        buy_item_form = BuyItemForm()

        return render(request, 'inventory/dashboard.html', {
            'items': items,
            'low_inventory_ids': low_inventory_ids,
            'buy_items': buy_items,
            'add_item_form': add_item_form,
            'buy_item_form': buy_item_form,
        })




class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/signup.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')
		else:
			messages.error(request,'Invalid User')

		return render(request, 'inventory/signup.html', {'form': form})



class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        """Returns the object to be edited."""
        obj = super().get_object(queryset)
        # Optionally, you can restrict editing only to specific users
        # if obj.user != self.request.user:
        #     raise PermissionDenied("You do not have permission to edit this item.")
        return obj

    def get_form_class(self):
        """Returns the form class to be used."""
        class DynamicForm(InventoryItemForm):
            class Meta:
                model = InventoryItem
                fields = ['user', 'image', 'unit_price']  # Include the 'user' field
        return DynamicForm

    def get_form_kwargs(self):
        """Returns the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        # Optionally, you can modify the form kwargs here
        return kwargs



class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'

class UpdateQuantityView(View):
    template_name = 'inventory/update_quantity.html'

    def get(self, request, product_id):
        name = InventoryItem.objects.get(id=product_id)
        form = QuantityUpdateForm()
        return render(request, self.template_name, {'form': form, 'name': name})

    def post(self, request, product_id):
        name = InventoryItem.objects.get(id=product_id)
        form = QuantityUpdateForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            name.quantity += quantity
            name.save()
            return redirect('dashboard')  # Redirect to your dashboard after updating
        return render(request, self.template_name, {'form': form, 'name': name})

class IssueQuantityView(View):
    template_name = 'inventory/issue_quantity.html'

    def get(self, request, product_id):
        name = InventoryItem.objects.get(id=product_id)
        form = QuantityIssueForm()
        return render(request, self.template_name, {'form': form, 'name': name})

    def post(self, request, product_id):
        name = InventoryItem.objects.get(id=product_id)
        form = QuantityUpdateForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            name.quantity -= quantity
            name.save()
            return redirect('dashboard')  # Redirect to your dashboard after updating
        return render(request, self.template_name, {'form': form, 'name': name})
    

from django.shortcuts import get_object_or_404, render
from django.views import View
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from decimal import Decimal
from .models import InventoryItem

class GenerateBillView(View):
    template_name = 'inventory/bill_template.html'

    def get_context_data(self, **kwargs):
        item = get_object_or_404(InventoryItem, pk=self.kwargs['pk'])
        total_price = Decimal(item.quantity) * item.unit_price
        gst_amount = total_price * Decimal('0.18') / 100  # 18% GST
        total_price_with_gst = total_price + gst_amount
        return {
            'item': item,
            'total_price': total_price,
            'gst_amount': gst_amount,
            'total_price_with_gst': total_price_with_gst,
            'user': self.request.user,
        }

    def render_to_pdf(self, context):
        template = get_template(self.template_name)
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="bill.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Failed to generate PDF: %s' % pisa_status.err)
        return response

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        pdf = self.render_to_pdf(context)
        return HttpResponse(pdf, content_type='application/pdf')







from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .forms import ForgotPasswordForm, OTPValidationForm, SetNewPasswordForm
from .models import PasswordResetOTP
import random
import string

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

class ForgotPasswordView(FormView):
    template_name = 'inventory/forgot_password.html'
    form_class = ForgotPasswordForm
    success_url = reverse_lazy('otp_validation')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            valid_until = timezone.now() + timezone.timedelta(minutes=10)  # OTP validity: 10 minutes
            PasswordResetOTP.objects.create(user=user, email=email, otp=otp, valid_until=valid_until)
            send_mail(
                'Password Reset OTP',
                f'Your OTP for resetting password is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return super().form_valid(form)
        except User.DoesNotExist:
            return redirect('forgot_password')  # Redirect back to the forgot password page if user does not exist



class OTPValidationView(FormView):
    template_name = 'inventory/otp_validation.html'
    form_class = OTPValidationForm
    success_url = reverse_lazy('set_new_password')

    def form_valid(self, form):
        otp = form.cleaned_data['otp']
        try:
            otp_record = PasswordResetOTP.objects.get(otp=otp, valid_until__gt=timezone.now())
            # Pass the OTP record to the success URL as a query parameter
            return redirect('set_new_password', otp_record=otp_record.pk)
        except PasswordResetOTP.DoesNotExist:
            form.add_error(None, 'Invalid OTP. Please try again.')  # Add error to form
            return render(self.request, self.template_name, {'form': form})






from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import SetNewPasswordForm

class SetNewPasswordView(LoginRequiredMixin, FormView):
    template_name = 'inventory/set_new_password.html'
    form_class = SetNewPasswordForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        new_password = form.cleaned_data['new_password']
        confirm_new_password = form.cleaned_data['confirm_new_password']
        
        if new_password == confirm_new_password:
            # Set the new password for the current user
            self.request.user.set_password(new_password)
            self.request.user.save()
            
            messages.success(self.request, 'Password updated successfully.')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Passwords do not match')
            return self.form_invalid(form)





from django.views.generic import ListView
from .models import InventoryItem
from .forms import InventorySearchForm

class InventorySearchView(ListView):
    model = InventoryItem
    template_name = 'inventory/inventory_search.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')
        
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search_query', '')
        return context



from django.db.models import F, Sum, Case, When, Value, IntegerField

from django.db.models import Sum


from django.views.generic import TemplateView
from .models import InventoryItem, SalesTransaction
from django.db.models import Sum

from django.db.models import DecimalField, ExpressionWrapper, F, Sum

class InventoryReportView(TemplateView):
    template_name = 'inventory/inventory_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Query inventory data
        inventory_items = InventoryItem.objects.annotate(
            total_amount=ExpressionWrapper(
                F('unit_price') * F('quantity'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            gst_amount=ExpressionWrapper(
                F('total_amount') * 0.18,
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            total_amount_with_gst=ExpressionWrapper(
                F('total_amount') + F('gst_amount'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )

        context['inventory_items'] = inventory_items

        return context



import io
import qrcode
from django.http import HttpResponse
from django.views import View
from .models import InventoryItem

class GenerateQRCodeView(View):
    def get(self, request, item_id):
        # Retrieve the inventory item
        try:
            item = InventoryItem.objects.get(id=item_id)
        except InventoryItem.DoesNotExist:
            return HttpResponse("Item not found", status=404)

        # Create BytesIO buffer to store the QR code image
        buffer = io.BytesIO()

        # Create QR code instance
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)

        # Add data to QR code (you can customize data as per your requirement)
        qr.add_data(f'Product ID: {item.id}\nName: {item.name}\nQuantity: {item.quantity}\nUnit Price: {item.unit_price}')

        # Make QR code
        qr.make(fit=True)

        # Create image from QR code
        img = qr.make_image(fill_color="limegreen", back_color="white")

        # Save image to buffer
        img.save(buffer, format='PNG')

        # Set the buffer pointer to the beginning
        buffer.seek(0)

        # Return the image as an HttpResponse
        return HttpResponse(buffer.getvalue(), content_type='image/png')


from django.shortcuts import render, redirect
from django.views.generic import View
from .models import InventoryItem, SalesTransaction

class SellView(View):
    template_name = 'inventory/sell_item.html'

    def get(self, request):
        available_items = InventoryItem.objects.filter(user=request.user)
        return render(request, self.template_name, {'available_items': available_items})

    def post(self, request):
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity'))
        sale_date = request.POST.get('sale_date')
        unit_price = float(request.POST.get('unit_price'))
        customer_name = request.POST.get('customer_name')  # Add this line
        mobile_number = request.POST.get('mobile_number')  # Add this line
        try:
            # Get the item object
            item = InventoryItem.objects.get(pk=item_id)

            # Check if requested quantity is available
            if item.quantity < quantity:
                raise ValueError("Requested quantity not available")

            # Deduct quantity from dashboard
            item.quantity -= quantity
            item.save()

            # Calculate total price and GST
            total_price = unit_price * quantity
            gst_amount = total_price * 0.18
            total_price_with_gst = total_price + gst_amount

            # Create a SalesTransaction object and save it
            sales_transaction = SalesTransaction.objects.create(
                inventory_item=item,
                user=request.user,
                quantity=quantity,
                total_price=total_price_with_gst,
                sale_date=sale_date,
                customer_name=customer_name,
                mobile_number=mobile_number
            )

            # Redirect to sales summary page with calculated details
            return redirect('generatesale_bill', 
                total_price=str(total_price), 
                gst_amount=str(gst_amount), 
                total_price_with_gst=str(total_price_with_gst),
                product_name=item.name, 
                quantity=quantity, 
                sale_date=sale_date, 
                unit_price=str(unit_price),
                customer_name=customer_name,  
                mobile_number=mobile_number)  

        except (InventoryItem.DoesNotExist, ValueError) as e:
            # Render error message if item or quantity is invalid
            return render(request, self.template_name, {'error_message': str(e), 'available_items': InventoryItem.objects.filter(user=request.user)})



class SalesSummaryView(View):
    template_name = 'inventory/sales_summary.html'

    def get(self, request, total_price, gst_amount, total_price_with_gst, product_name, quantity, sale_date, unit_price, customer_name, mobile_number):
        # Convert captured values to floats if needed
        total_price = float(total_price)
        gst_amount = float(gst_amount)
        total_price_with_gst = float(total_price_with_gst)
        
        # For demonstration purposes, I'll create placeholders for the blank fields
        # Render the sales summary template with the calculated values and blank fields
        return render(request, self.template_name, {
            'total_price': total_price,
            'gst_amount': gst_amount,
            'total_price_with_gst': total_price_with_gst,
            'product_name': product_name,
            'quantity': quantity,
            'sale_date': sale_date,
            'unit_price': unit_price,
            'customer_name': customer_name,  # Add this line
            'mobile_number': mobile_number,  # Add this line
        })


from django.shortcuts import render
from django.views import View

class GenerateSaleBillView(View):
    template_name = 'inventory/generatesale_bill.html'

    def get(self, request, **kwargs):
        # Fetch data from kwargs and convert to appropriate types
        product_name = kwargs.get('product_name', '')
        quantity = int(kwargs.get('quantity', 0))
        sale_date = kwargs.get('sale_date', '')
        unit_price = float(kwargs.get('unit_price', '0.0'))
        total_price = float(kwargs.get('total_price', '0.0'))
        gst_amount = float(kwargs.get('gst_amount', '0.0'))
        total_price_with_gst = float(kwargs.get('total_price_with_gst', '0.0'))
        customer_name = kwargs.get('customer_name', '')
        mobile_number = kwargs.get('mobile_number', '')

        # Render the generate bill template with the data
        return render(request, self.template_name, {
            'product_name': product_name,
            'quantity': quantity,
            'sale_date': sale_date,
            'unit_price': unit_price,
            'total_price': total_price,
            'gst_amount': gst_amount,
            'total_price_with_gst': total_price_with_gst,
            'customer_name': customer_name,
            'mobile_number': mobile_number,
        })


import io
from barcode import Code128
from barcode.writer import ImageWriter
from django.http import HttpResponse
from django.views import View
from .models import InventoryItem

class GenerateBarcodeView(View):
    def get(self, request, item_id):
        # Retrieve the inventory item
        try:
            item = InventoryItem.objects.get(id=item_id)
        except InventoryItem.DoesNotExist:
            return HttpResponse("Item not found", status=404)

        # Format data
        data = f'{item.id}{item.name}'

        # Generate barcode object
        barcode_img = Code128(data, writer=ImageWriter())

        # Save barcode image to BytesIO buffer
        barcode_buffer = io.BytesIO()
        barcode_img.write(barcode_buffer)

        # Set the buffer pointer to the beginning
        barcode_buffer.seek(0)

        # Return the barcode image as an HttpResponse
        return HttpResponse(barcode_buffer.getvalue(), content_type='image/png')


#Sale multiple product
# views.py

from django.shortcuts import render
from django.views.generic import View
from decimal import Decimal
from .models import InventoryItem, SalesTransaction

class SellMultipleItemsView(View):
    template_name = 'inventory/sell_multiple_items.html'

    def get(self, request):
        available_items = InventoryItem.objects.filter(user=request.user)
        return render(request, self.template_name, {'available_items': available_items})

    def post(self, request):
        item_ids = request.POST.getlist('item_id[]')
        quantities = request.POST.getlist('quantity[]')
        sale_date = request.POST.get('sale_date')
        unit_prices = request.POST.getlist('unit_price[]')
        customer_name = request.POST.get('customer_name')
        mobile_number = request.POST.get('mobile_number')

        customer_name = str(customer_name)
        mobile_number = str(mobile_number)
        total_price = Decimal('0')
        gst_amount = Decimal('0')
        total_price_with_gst = Decimal('0')
        sales_transactions = []

        for item_id, quantity, unit_price in zip(item_ids, quantities, unit_prices):
            item = InventoryItem.objects.get(pk=item_id)

            # Check if requested quantity is available
            if item.quantity < int(quantity):
                raise ValueError(f"Requested quantity of {item.name} not available")

            total_price_item = Decimal(unit_price) * Decimal(quantity)
            gst_amount_item = total_price_item * Decimal('0.18')
            total_price_with_gst_item = total_price_item + gst_amount_item

            # Create a SalesTransaction object and save it
            sales_transaction = SalesTransaction.objects.create(
                inventory_item=item,
                user=request.user,
                quantity=int(quantity),
                total_price=total_price_with_gst_item,
                sale_date=sale_date,
                customer_name=customer_name,
                mobile_number=mobile_number
            )
            sales_transactions.append(sales_transaction)

            # Deduct quantity from dashboard
            item.quantity -= int(quantity)
            item.save()

            # Calculate total price and GST
            total_price += total_price_item
            gst_amount += gst_amount_item
            total_price_with_gst += total_price_with_gst_item

        return render(request, 'inventory/generatesale_bill1.html', {
            'summaries': sales_transactions,
            'total_price': total_price,
            'gst_amount': gst_amount,
            'total_price_with_gst': total_price_with_gst,
            'customer_name': customer_name,
            'mobile_number': mobile_number,
        })


# views.py

from django.shortcuts import render
from django.views.generic import View

class GenerateSaleBillView1(View):
    template_name = 'inventory/generatesale_bill1.html'

    def get(self, request, product_name, quantity, sale_date, unit_price, total_price, gst_amount, total_price_with_gst, customer_name, mobile_number):
        context = {
            'product_name': product_name,
            'quantity': quantity,
            'sale_date': sale_date,
            'unit_price': unit_price,
            'total_price': total_price,
            'gst_amount': gst_amount,
            'total_price_with_gst': total_price_with_gst,
            'customer_name': customer_name,
            'mobile_number': mobile_number,
        }
        return render(request, self.template_name, context)


from django.shortcuts import render
from django.views.generic import View
from .models import SalesTransaction

class SalesReportView(View):
    template_name = 'inventory/sales_report.html'

    def get(self, request):
        # Retrieve all sales transactions
        sales_transactions = SalesTransaction.objects.all()

        # Calculate grand total price
        grand_total_price = sum(sale.total_price for sale in sales_transactions)

        context = {
            'sales_transactions': sales_transactions,
            'grand_total_price': grand_total_price,
        }

        return render(request, self.template_name, context)


from django.db.models import Sum
from django.contrib.auth.models import User

def user_list(request):
    # Get all users
    users = User.objects.all()

    # Calculate total amount for each user
    for user in users:
        total_amount = SalesTransaction.objects.filter(user=user).aggregate(total_amount=Sum('total_price'))['total_amount']
        user.total_amount = total_amount if total_amount else 0

    return render(request, 'inventory/user_list.html', {'users': users})



# views.py

from django.shortcuts import render, redirect
from .forms import BuyItemForm,SellMultipleItemsForm

def buy_items(request):
    if request.method == 'POST':
        form = BuyItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard after buying items
    else:
        form = BuyItemForm()
    return render(request, 'inventory/buy_items.html', {'form': form})


from django.shortcuts import render
from django.views.generic import View
from .models import BoughtItem

class BuyReportView(View):
    template_name = 'inventory/buy_report.html'

    def get(self, request):
        # Retrieve all bought items
        bought_items = BoughtItem.objects.all()

        # Calculate total spent
        total_spent = sum(item.total_price for item in bought_items)

        context = {
            'bought_items': bought_items,
            'total_spent': total_spent,
        }

        return render(request, self.template_name, context)


