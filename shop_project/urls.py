# shop_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views  # Import views from your core app


from django.contrib import admin

admin.site.site_header = "ShopMaster Administration"
admin.site.site_title = "ShopMaster Admin Portal"
admin.site.index_title = "Welcome to ShopMaster Database"

urlpatterns = [
    # 1. Admin Panel
    path('admin/', admin.site.urls),
    
    # 2. Traffic Controller (Redirects after login)
    path('login-redirect/', views.login_redirect_view, name='login_redirect'),
    
    # 3. Authentication (Login, Logout, Password Reset)
    path('accounts/', include('django.contrib.auth.urls')),
    
   
    path('inventory/', views.inventory_view, name='inventory'),
    path('daily-sales/', views.daily_sales_view, name='daily_sales'),
    path('profit-loss/', views.profit_loss_view, name='profit_loss'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('reports/', views.reports_view, name='reports'),
    path('customers/', views.customers_view, name='customers'),
    path('staff/', views.staff_view, name='staff'),
    path('suppliers/', views.suppliers_view, name='suppliers'),
    path('invoice/', views.invoice_view, name='invoice'),

   
    path('', include('core.urls')), 
]

# This allows images to be displayed in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)