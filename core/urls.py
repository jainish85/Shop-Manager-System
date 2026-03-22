from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    # Dashboard
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    
      path('register-staff/', views.register_staff, name='register_staff'),
      path('accounts/register/', views.register_user, name='register'),
      
    # Inventory & Products
    path('inventory/', views.inventory_view, name='inventory'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # Categories
    path('add-category/', views.add_category, name='add_category'),
    path('categories/', views.manage_categories, name='manage_categories'),
    path('delete-category/<int:pk>/', views.delete_category, name='delete_category'),

    # Sales & Transactions
    path('sell/<int:pk>/', views.sell_product, name='sell_product'),
    path('daily-sales/', views.daily_sales_view, name='daily_sales'), # Linked correctly
    path('sales-history/', views.sales_history, name='sales_history'),

    # Finance
    path('profit-loss/', views.profit_loss_view, name='profit_loss'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('expenses/delete/<int:pk>/', views.delete_expense, name='delete_expense'),

    # Others
    path('profile/', views.profile, name='profile'),
    path('reports/', views.reports_view, name='reports'),  
    #invoice
    path('invoice/', views.invoice_view, name='invoice'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'),


    #suppliers
    path('suppliers/', views.suppliers_view, name='suppliers'),
    path('suppliers/update/<int:pk>/', views.update_supplier, name='update_supplier'),
    path('suppliers/delete/<int:pk>/', views.delete_supplier, name='delete_supplier'),

    #stff
    path('staff/', views.staff_view, name='staff'),
    path('staff/update/<int:pk>/', views.update_staff, name='update_staff'),
    path('staff/delete/<int:pk>/', views.delete_staff, name='delete_staff'),

    #customers
    path('customers/', views.customers_view, name='customers'),
    path('customers/update/<int:pk>/', views.update_customer, name='update_customer'),
    path('customers/delete/<int:pk>/', views.delete_customer, name='delete_customer'), 
]