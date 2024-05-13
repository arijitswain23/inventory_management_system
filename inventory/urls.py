from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    #path('profile', Profile.as_view(), name='profile'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('add-item/', AddItem.as_view(), name='add-item'),
    path('edit-item/<int:pk>', EditItem.as_view(), name='edit-item'),
    path('delete-item/<int:pk>', DeleteItem.as_view(), name='delete-item'),
    #path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='inventory/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
    path('update_quantity/<int:product_id>/', UpdateQuantityView.as_view(), name='update_quantity'),
    path('issue_quantity/<int:product_id>/', IssueQuantityView.as_view(), name='issue_quantity'),
    path('generate-bill/<int:pk>/', GenerateBillView.as_view(), name='generate_bill'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    #path('forgot_password_done/', ForgotPasswordDoneView.as_view(), name='forgot_password_done'),
    path('otp_validation/', OTPValidationView.as_view(), name='otp_validation'),
    path('set_new_password/<int:otp_record>/', SetNewPasswordView.as_view(), name='set_new_password'),
    #path('set_new_password/', SetNewPasswordView.as_view(), name='set_new_password'),
    #path('password_reset_confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm')
    #path('password_reset_error/',PasswordResetErrorView.as_view(),name="password_reset_error"),
    path('inventory/search/', InventorySearchView.as_view(), name='inventory_search'),
    path('inventory/report/', InventoryReportView.as_view(), name='inventory_report'),
    path('inventory/salesreport/', SalesReportView.as_view(), name='sales_report'),

    path('generate-qrcode/<int:item_id>/', GenerateQRCodeView.as_view(), name='generate_qrcode'),
    path('thanku/',Thanku.as_view(),name='thanku'),
    path('sell/', SellView.as_view(), name='sell'),
    #path('sales-summary/<total_price>/<gst_amount>/<total_price_with_gst>/', SalesSummaryView.as_view(), name='sales_summary'),
    #path('sales_summary/<float:total_price>/<float:gst_amount>/<float:total_price_with_gst>/<str:product_name>/<int:quantity>/<str:sale_date>/<float:unit_price>/', SalesSummaryView.as_view(), name='sales_summary'),
    #path('sales_summary/<str:total_price>/<str:gst_amount>/<str:total_price_with_gst>/<str:product_name>/<int:quantity>/<str:sale_date>/<str:unit_price>/', SalesSummaryView.as_view(), name='sales_summary'),
    #path('generatesale-bill/<str:product_name>/<int:quantity>/<str:sale_date>/<str:unit_price>/<str:total_price>/<str:gst_amount>/<str:total_price_with_gst>/', GenerateSaleBillView.as_view(), name='generatesale_bill'),
    #path('fetch-product/<int:item_id>/', FetchProductDetailsView.as_view(), name='fetch_product'),
    path('sales_summary/<str:total_price>/<str:gst_amount>/<str:total_price_with_gst>/<str:product_name>/<int:quantity>/<str:sale_date>/<str:unit_price>/<str:customer_name>/<str:mobile_number>/', SalesSummaryView.as_view(), name='sales_summary'),
    path('generatesale_bill/<str:product_name>/<int:quantity>/<str:sale_date>/<str:unit_price>/<str:total_price>/<str:gst_amount>/<str:total_price_with_gst>/<str:customer_name>/<str:mobile_number>/', GenerateSaleBillView.as_view(), name='generatesale_bill'),
    path('generate-barcode/<int:item_id>',GenerateBarcodeView.as_view(),name='generate_barcode'),
    #path('dashboard1/', Dashboard1.as_view(), name='dashboard1'),
    #path('sale/<int:item_id>/', SaleView.as_view(), name='sale'),
    #path('sell1/', SellView1.as_view(), name='sell1'),
    #path('sales-summary1/', SalesSummaryView1.as_view(), name='sales_summary1'),
    #path('generate-sale-bill1/<int:sale_id>/', GenerateSaleBillView1.as_view(), name='generate_sale_bill1'),
    path('generate-bill/<int:sales_record_id>/', GenerateBillView.as_view(), name='generate_bill'),
    #path('get-unit-price/', GetUnitPriceView.as_view(), name='get_unit_price'),
    path('sell1/', SellMultipleItemsView.as_view(), name='sell1'),
    path('generatesale_bill1/<str:product_name>/<int:quantity>/<str:sale_date>/<str:unit_price>/<str:total_price>/<str:gst_amount>/<str:total_price_with_gst>/<str:customer_name>/<str:mobile_number>/', GenerateSaleBillView1.as_view(), name='generatesale_bill1'),
    path('user_list/',user_list,name='user_list'),
    path('buy_items/',buy_items,name='buy_items'),
    path('buy_report/',BuyReportView.as_view(),name='buy_report'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)