from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    # Dashboard
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    
path('register-staff/', views.register_staff, name='register_staff'),
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
    path('customers/', views.customers_view, name='customers'),
    path('staff/', views.staff_view, name='staff'),
    path('suppliers/', views.suppliers_view, name='suppliers'),
    path('invoice/', views.invoice_view, name='invoice'),
]