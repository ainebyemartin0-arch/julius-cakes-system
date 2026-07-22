from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from .models import Product, Category, Order
from datetime import date

def index(request):
    featured_products = Product.objects.all()[:3]
    return render(request, 'index.html', {'featured_products': featured_products})

def catalog(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'catalog.html', {'categories': categories, 'products': products})

def custom_order(request):
    if request.method == 'POST':
        flavor = request.POST.get('flavor')
        size = request.POST.get('size')
        message = request.POST.get('message')
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        delivery_option = request.POST.get('delivery_option')
        required_date = request.POST.get('required_date')
        
        cake_details = f"Flavor: {flavor}, Size: {size}, Message: {message}"
        
        order = Order(
            customer_name=customer_name,
            customer_phone=customer_phone,
            delivery_option=delivery_option,
            required_date=required_date,
            cake_details=cake_details,
            status='pending'
        )
        
        if 'reference_image' in request.FILES:
            order.reference_image = request.FILES['reference_image']
            
        order.save()
        return redirect('order_success', order_id=order.id)

    return render(request, 'custom_order.html')

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_success.html', {'order': order})

def track_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        phone = request.POST.get('customer_phone')
        
        try:
            order = Order.objects.get(id=order_id, customer_phone=phone)
            return render(request, 'track_order.html', {'order': order, 'searched': True})
        except Order.DoesNotExist:
            return render(request, 'track_order.html', {'error': 'Order not found. Please check your Order ID and Phone number.', 'searched': True})
            
    return render(request, 'track_order.html')

@staff_member_required
def staff_dashboard(request):
    # Calculate Analytics
    total_revenue = Order.objects.filter(status='completed').aggregate(Sum('total_price'))['total_price__sum'] or 0
    pending_orders = Order.objects.filter(status='pending').count()
    baking_orders = Order.objects.filter(status='baking').count()
    todays_bakes = Order.objects.exclude(status='completed').filter(required_date=date.today())
    
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'baking_orders': baking_orders,
        'todays_bakes': todays_bakes,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard.html', context)

# Custom Error Handlers
def custom_404(request, exception=None):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)
