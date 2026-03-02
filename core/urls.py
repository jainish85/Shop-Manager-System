from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),

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

    # Finance
    path('profit-loss/', views.profit_loss_view, name='profit_loss'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('expenses/delete/<int:pk>/', views.delete_expense, name='delete_expense'),

    # Others
    path('profile/', views.profile, name='profile'),
    path('reports/', views.reports_view, name='reports'),
 
    path('customers/', views.customers_view, name='customers'),
    path('customers/delete/<int:pk>/', views.delete_customer, name='delete_customer'), 
    path('customers/update/<int:pk>/', views.update_customer, name='update_customer'),
 
    path('staff/', views.staff_view, name='staff'),
    path('staff/update/<int:pk>/', views.update_staff, name='update_staff'),
    path('staff/delete/<int:pk>/', views.delete_staff, name='delete_staff'),
 
    path('suppliers/', views.suppliers_view, name='suppliers'),
    path('suppliers/delete/<int:pk>/', views.delete_supplier, name='delete_supplier'), 
    path('suppliers/update/<int:pk>/', views.update_supplier, name='update_supplier'),
 
    path('invoice/', views.invoice_view, name='invoice'),
    path('invoice/<int:pk>/', views.invoice_detail, name='invoice_detail'), 

    path('reports/', views.reports_and_ai, name='reports'),

    path('reports-ai/', views.ai_forecast_view, name='reports')

]