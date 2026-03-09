import datetime
from datetime import timedelta
import calendar
from django.utils import timezone
from django.db.models import Sum, Count, F, Q
from django.db.models.functions import TruncDay, TruncMonth


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Product, Category, Sale, Expense ,Customer ,Staff ,Supplier ,Invoice ,InvoiceItem
from .forms import ProductForm, CategoryForm, SaleForm, ExpenseForm ,CustomerForm ,StaffForm ,SupplierForm ,InvoiceForm, InvoiceItemForm



def login_redirect_view(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        return redirect('home')

@login_required
def register_staff(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register_staff')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        user.is_staff = True
        user.save()

        messages.success(request, "Staff account created successfully!")
        return redirect('staff')

    return render(request, 'core/register.html')

# --- DASHBOARD / HOME ---
@login_required
def home(request):
    today = timezone.now().date()
    todays_sales_data = Sale.objects.filter(sale_date__date=today).aggregate(Sum('total_price'), Count('id'))
    todays_sales = todays_sales_data['total_price__sum'] or 0
    todays_orders = todays_sales_data['id__count'] or 0
    
    total_products = Product.objects.count()
    total_value_data = Product.objects.aggregate(total=Sum(F('price') * F('stock_quantity')))
    total_value = total_value_data['total'] or 0
    
    low_stock_products = Product.objects.filter(stock_quantity__lt=5)
    low_stock_count = low_stock_products.count()
    
    dates = []
    sales_counts = []
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime("%a"))
        day_sales = Sale.objects.filter(sale_date__date=date).aggregate(Sum('total_price'))['total_price__sum'] or 0
        sales_counts.append(float(day_sales))
        
    recent_sales = Sale.objects.select_related('product', 'sold_by').order_by('-sale_date')[:5]

    context = {
        'todays_sales': todays_sales,
        'todays_orders': todays_orders,
        'total_products': total_products,
        'total_value': total_value,
        'low_stock_count': low_stock_count,
        'chart_dates': dates,
        'chart_sales': sales_counts,
        'low_stock_products': low_stock_products[:5],
        'recent_sales': recent_sales,
    }
    return render(request, 'core/home.html', context)


@login_required
def daily_sales_view(request):
    if not request.user.is_superuser:
            raise PermissionDenied

    today = timezone.now().date()
    
    sales_today = Sale.objects.filter(sale_date__date=today).order_by('-sale_date')
    
    total_revenue = sales_today.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_items = sales_today.aggregate(Sum('quantity'))['quantity__sum'] or 0

    context = {
        'sales': sales_today,
        'total_revenue': total_revenue,
        'total_items': total_items,
        'today': today,
    }

    return render(request, 'core/daily_sales.html', context)

# --- ADD PRODUCT ---
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.cost_price = request.POST.get('cost_price', 0)
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('inventory')
    else:
        form = ProductForm()
    return render(request, 'core/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            prod = form.save(commit=False)
            cost = request.POST.get('cost_price')
            if cost:
                prod.cost_price = cost
            prod.save()
            return redirect('inventory')
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/add_product.html', {'form': form})

@login_required
def delete_product(request, pk):
    if not request.user.is_superuser:
        raise PermissionDenied  
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted.")
    return redirect('inventory')



# --- CATEGORY MANAGEMENT ---
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_product')
    else:
        form = CategoryForm()
    return render(request, 'core/add_category.html', {'form': form})

@login_required
def manage_categories(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'core/manage_categories.html', {'categories': categories, 'form': form})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('manage_categories')



# --- SELL PRODUCT ---
@login_required
def sell_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            quantity_sold = form.cleaned_data['quantity']
            if product.stock_quantity >= quantity_sold:
                product.stock_quantity -= quantity_sold
                product.save()
                
                sale = form.save(commit=False)
                sale.product = product
                sale.total_price = product.price * quantity_sold
                sale.sold_by = request.user
                sale.save()
                
                messages.success(request, f"Sold {quantity_sold} of {product.name}!")
                return redirect('daily_sales') # Updated redirect
            else:
                messages.error(request, "Not enough stock!")
    else:
        form = SaleForm()
    return render(request, 'core/sell_product.html', {'product': product, 'form': form})


# --- INVENTORY VIEW ---
@login_required
def inventory_view(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(category__name__icontains=query))
    else:
        products = Product.objects.all()
    return render(request, 'core/inventory.html', {'products': products})




# --- PROFIT & LOSS VIEW --- 
@login_required
def profit_loss_view(request):
    today = timezone.now().date()
    current_year = today.year
    monthly_report = []
    
    total_revenue_year = 0
    total_cogs_year = 0
    total_opex_year = 0
    
    for m in range(1, 13):
        if m > today.month: 
            break # Don't show future months
        
        # Superpower added here: select_related('product') makes this lightning fast!
        monthly_sales = Sale.objects.filter(
            sale_date__year=current_year, 
            sale_date__month=m
        ).select_related('product')
        
        revenue = monthly_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        # Calculate COGS
        cogs = sum((s.product.cost_price * s.quantity) for s in monthly_sales if s.product)
        
        monthly_expenses = Expense.objects.filter(
            date_added__year=current_year, 
            date_added__month=m
        )
        opex = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        
        gross_profit = revenue - cogs
        net_profit = gross_profit - opex
        
        total_revenue_year += revenue
        total_cogs_year += cogs
        total_opex_year += opex
        
        month_name = datetime.date(current_year, m, 1).strftime('%b')
        
        monthly_report.append({
            'month': month_name, 
            'revenue': revenue, 
            'cogs': cogs,
            'gross_profit': gross_profit, 
            'expenses': opex, 
            'net_profit': net_profit
        })

    total_gross_profit = total_revenue_year - total_cogs_year
    total_net_profit = total_gross_profit - total_opex_year
    profit_margin = (total_net_profit / total_revenue_year * 100) if total_revenue_year > 0 else 0

    context = {
        'current_year': current_year,
        'monthly_report': monthly_report,
        'total_revenue': total_revenue_year,
        'total_expenses': total_opex_year, 
        'gross_profit': total_gross_profit,
        'net_profit': total_net_profit,
        'profit_margin': profit_margin,
    }
    return render(request, 'core/profit_loss.html', context)




# --- EXPENSES VIEW ---
@login_required
def expenses_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.added_by = request.user
            expense.save()
            messages.success(request, "Expense added!")
            return redirect('expenses')
    else:
        form = ExpenseForm()
    expenses = Expense.objects.all().order_by('-date_added')
    return render(request, 'core/expenses.html', {'form': form, 'expenses': expenses})

@login_required
def delete_expense(request, pk):
    get_object_or_404(Expense, pk=pk).delete()
    return redirect('expenses')


# --- PLACEHOLDERS ---
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'core/product_detail.html', {'product': product})

@login_required
def profile(request):
    return render(request, 'core/profile.html')

@login_required
def reports_view(request): return render(request, 'core/reports.html')


@login_required
def customers_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer added successfully!")
            return redirect('customers')
    else:
        form = CustomerForm()
    
    customers = Customer.objects.all().order_by('-date_added')
    return render(request, 'core/customers.html', {'form': form, 'customers': customers})

@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.delete()
    messages.success(request, f"Customer {customer.name} deleted successfully!")
    return redirect('customers')

@login_required
def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer '{customer.name}' updated successfully!")
            return redirect('customers')
    else:
        form = CustomerForm(instance=customer)
        
    return render(request, 'core/update_customer.html', {'form': form, 'customer': customer})



#staf views page
@login_required
def staff_view(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New staff member hired!")
            return redirect('staff')
    else:
        form = StaffForm()
    
    staff_list = Staff.objects.all()
    return render(request, 'core/staff.html', {'form': form, 'staff_list': staff_list})

@login_required
def update_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, f"Staff member updated successfully!")
            return redirect('staff') 
    else:
        form = StaffForm(instance=staff)
    return render(request, 'core/update_staff.html', {'form': form, 'staff': staff})

@login_required
def delete_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff.delete()
        messages.success(request, "Staff member deleted successfully!")
    return redirect('staff')


#spplier views page
@login_required
def suppliers_view(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Supplier added successfully!")
            return redirect('suppliers')
    else:
        form = SupplierForm()
    
    suppliers = Supplier.objects.all().order_by('-date_added')
    return render(request, 'core/suppliers.html', {'form': form, 'suppliers': suppliers})

@login_required
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        supplier_name = supplier.company_name 
        supplier.delete()
        messages.success(request, f"Supplier '{supplier_name}' deleted successfully!")
        
    return redirect('suppliers')

@login_required
def update_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, f"Supplier '{supplier.company_name}' updated successfully!")
            return redirect('suppliers')
    else:
        form = SupplierForm(instance=supplier)
        
    return render(request, 'core/update_supplier.html', {'form': form, 'supplier': supplier})



#invoice view
@login_required
def invoice_view(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            messages.success(request, "Invoice created! Now add products.")
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
    
    invoices = Invoice.objects.all().order_by('-date_created')
    return render(request, 'core/invoice.html', {'form': form, 'invoices': invoices})

@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        form = InvoiceItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.invoice = invoice
            item.price = item.product.price 
            
            if item.product.stock_quantity >= item.quantity:
                item.save()
                invoice.total_amount += item.get_total()
                invoice.save()               
                item.product.stock_quantity -= item.quantity
                item.product.save()
                
                messages.success(request, f"Added {item.quantity} x {item.product.name} to bill.")
            else:
                messages.error(request, f"Not enough stock for {item.product.name}!")
            
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceItemForm()
        
    return render(request, 'core/invoice_detail.html', {'invoice': invoice, 'form': form})



# Reports & AI

@login_required
def reports_and_ai(request):
    total_customers = Customer.objects.count()
    total_suppliers = Supplier.objects.count()
    total_staff = Staff.objects.count()
    
    total_payroll = Staff.objects.aggregate(Sum('salary'))['salary__sum'] or 0

    ai_insights = []
    
    if total_customers < 5:
        ai_insights.append("📈 **Growth Alert:** Customer base is small. Consider a local marketing campaign to attract more buyers.")
    else:
        ai_insights.append(f"🌟 **Great job!** You have a solid base of {total_customers} customers. Time to start a loyalty program.")
        
    if total_staff > 0 and total_payroll > 0:
        avg_salary = total_payroll / total_staff
        ai_insights.append(f"₹ **Payroll Insight:** Your average employee salary is ₹ {avg_salary:,.2f}. Keep an eye on revenue to ensure payroll stays under 30% of your total expenses.")
    
    if total_suppliers < 2:
        ai_insights.append("⚠️ **Risk Warning:** Relying on too few suppliers. Consider adding backup suppliers to prevent stock shortages.")

    context = {
        'total_customers': total_customers,
        'total_suppliers': total_suppliers,
        'total_staff': total_staff,
        'total_payroll': total_payroll,
        'ai_insights': ai_insights,
    }
    return render(request, 'core/reports.html', context)



# --- THE AI MATH ENGINE ---
def calculate_future_projections(data_list, periods=3):
    """
    Takes a list of historical numbers (like past 6 months revenue) 
    and predicts the next 'periods' months using WMA + Growth Rate.
    """
    if len(data_list) < 2:
        return [0] * periods # Not enough data to predict

    # 1. Calculate Weighted Moving Average (WMA)
    # Give higher weight to recent months [1, 2, 3, 4, 5, 6]
    weights = list(range(1, len(data_list) + 1)) 
    weight_sum = sum(weights)
    
    wma = sum(data * weight for data, weight in zip(data_list, weights)) / weight_sum

    # 2. Calculate Average Month-over-Month Growth Rate
    growth_rates = []
    for i in range(1, len(data_list)):
        prev = data_list[i-1]
        curr = data_list[i]
        if prev > 0:
            growth_rates.append((curr - prev) / prev)
        else:
            growth_rates.append(0)
            
    avg_growth = sum(growth_rates) / len(growth_rates) if growth_rates else 0
    
    # Cap growth at realistically safe boundaries (e.g., max +/- 15% per month)
    # We don't want the AI promising you a trillion dollars next year!
    avg_growth = max(min(avg_growth, 0.15), -0.15) 

    forecast = []
    current_base = wma
    for _ in range(periods):
        next_val = current_base * (1 + avg_growth)
        forecast.append(round(next_val, 2))
        current_base = next_val

    return forecast

# --- UPDATE YOUR VIEW ---
@login_required
def ai_forecast_view(request):
    # Let's get the last 6 months of data
    today = timezone.now().date()
    
    historical_revenue = []
    historical_expenses = []
    future_months = []
    
    # 1. Gather the last 6 months of data from your database
    for i in range(5, -1, -1):
        target_date = today - timedelta(days=30*i)
        
        monthly_sales = Sale.objects.filter(sale_date__year=target_date.year, sale_date__month=target_date.month)
        rev = monthly_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        monthly_exp = Expense.objects.filter(date_added__year=target_date.year, date_added__month=target_date.month)
        exp = monthly_exp.aggregate(Sum('amount'))['amount__sum'] or 0
        
        historical_revenue.append(float(rev))
        historical_expenses.append(float(exp))

    # 2. Feed data into our Prediction Engine!
    predicted_revenue = calculate_future_projections(historical_revenue, periods=3)
    predicted_expenses = calculate_future_projections(historical_expenses, periods=3)
    
    # Calculate predicted Net Profit
    predicted_net_profit = [round(rev - exp, 2) for rev, exp in zip(predicted_revenue, predicted_expenses)]

    # 3. Get the names of the next 3 months for the chart (e.g., "Apr", "May", "Jun")
    for i in range(1, 4):
        next_month = (today.replace(day=1) + timedelta(days=32*i)).replace(day=1)
        future_months.append(calendar.month_abbr[next_month.month])

    context = {
        'future_months': future_months,
        'predicted_revenue': predicted_revenue,
        'predicted_expenses': predicted_expenses,
        'predicted_net_profit': predicted_net_profit,
        
        'next_month_revenue': predicted_revenue[0] if predicted_revenue else 0,
        'next_month_profit': predicted_net_profit[0] if predicted_net_profit else 0,
    }
    
    return render(request, 'core/predictions.html', context)