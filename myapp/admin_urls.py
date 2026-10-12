from django.urls import path
from . import admin_views

urlpatterns = [
    # Dashboard Overview
    path('', admin_views.admin_dashboard, name='admin_dashboard'),

    # Product Management
    path('products/', admin_views.admin_products, name='admin_products'),
    path('products/add/', admin_views.admin_product_add, name='admin_product_add'),
    path('products/edit/<int:product_id>/', admin_views.admin_product_edit, name='admin_product_edit'),
    path('products/delete/<int:product_id>/', admin_views.admin_product_delete, name='admin_product_delete'),
    path('products/toggle-stock/<int:product_id>/', admin_views.admin_product_toggle_stock, name='admin_product_toggle_stock'),
    path('products/toggle-active/<int:product_id>/', admin_views.admin_product_toggle_active, name='admin_product_toggle_active'),

    # Categories & Brands
    path('categories/', admin_views.admin_categories, name='admin_categories'),

    # Order Management
    path('orders/', admin_views.admin_orders, name='admin_orders'),
    path('orders/<str:order_id>/', admin_views.admin_order_detail, name='admin_order_detail'),
    path('orders/update-status/<str:order_id>/', admin_views.admin_order_update_status, name='admin_order_update_status'),

    # Customer Management
    path('customers/', admin_views.admin_customers, name='admin_customers'),
    path('customers/<int:customer_id>/', admin_views.admin_customer_detail, name='admin_customer_detail'),

    # Inventory
    path('inventory/', admin_views.admin_inventory, name='admin_inventory'),

    # Coupons
    path('coupons/', admin_views.admin_coupons, name='admin_coupons'),

    # Reviews
    path('reviews/', admin_views.admin_reviews, name='admin_reviews'),

    # Analytics
    path('analytics/', admin_views.admin_analytics, name='admin_analytics'),

    # Settings
    path('settings/', admin_views.admin_settings_view, name='admin_settings'),
]
