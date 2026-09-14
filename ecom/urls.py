
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from myapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("myapp.urls")),
    path('checkout_cart/<str:slug>/', views.checkout_cart, name='checkout_cart'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

urlpatterns += staticfiles_urlpatterns()