from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from app.views import (
    RoleListCreateView, RoleRetrieveUpdateDestroyView,
    UserListCreateView, UserRetrieveUpdateDestroyView, CurrentUserView,
    ProductTypeListCreateView, ProductTypeRetrieveUpdateDestroyView,
    ProductListCreateView, ProductRetrieveUpdateDestroyView,
    OrderProductListCreateView, OrderProductRetrieveUpdateDestroyView,
    StatusListCreateView, StatusRetrieveUpdateDestroyView,
    OrderListCreateView, OrderRetrieveUpdateDestroyView, ChangeOrderStatusView,
    LoginView, ChangePasswordView
)

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Your API",
      default_version='v1',
      description="API documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@yourapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Your existing URLs
    path('roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleRetrieveUpdateDestroyView.as_view(), name='role-detail'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('me/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('product-types/', ProductTypeListCreateView.as_view(), name='product-type-list-create'),
    path('product-types/<int:pk>/', ProductTypeRetrieveUpdateDestroyView.as_view(), name='product-type-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('order-products/', OrderProductListCreateView.as_view(), name='order-product-list-create'),
    path('order-products/<int:pk>/', OrderProductRetrieveUpdateDestroyView.as_view(), name='order-product-detail'),
    path('statuses/', StatusListCreateView.as_view(), name='status-list-create'),
    path('statuses/<int:pk>/', StatusRetrieveUpdateDestroyView.as_view(), name='status-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('orders/<int:pk>/change-status/', ChangeOrderStatusView.as_view(), name='order-change-status'),
    path('login/', LoginView.as_view(), name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)