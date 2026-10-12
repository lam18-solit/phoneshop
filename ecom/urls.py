
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from myapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from myapp.admin_views import admin_login_view, admin_logout_view

urlpatterns = [
    # Phone Shop Custom Admin Dashboard
    path('admin/login/', admin_login_view, name='admin_login'),
    path('admin/logout/', admin_logout_view, name='admin_logout'),
    path('admin/dashboard/', include('myapp.admin_urls')),

    # Default Django admin
    path('admin/', admin.site.urls),
    path("", include("myapp.urls")),
    path('checkout_cart/<str:slug>/', views.checkout_cart, name='checkout_cart'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += staticfiles_urlpatterns()