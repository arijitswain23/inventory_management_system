from django.contrib import admin
from .models import *

admin.site.register(InventoryItem)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(SalesTransaction)
admin.site.register(PasswordResetOTP)
#admin.site.register(QuantityAdjustment)
#admin.site.register(SalesItem)
admin.site.register(Supplier)
admin.site.register(BoughtItem)

