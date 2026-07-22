from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog', views.catalog, name='catalog'),
    path('custom-order', views.custom_order, name='custom_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('track', views.track_order, name='track_order'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
]
