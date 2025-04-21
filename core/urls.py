from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.views import (
    RoleListCreateView, RoleRetrieveUpdateDestroyView,
    UserListCreateView, UserRetrieveUpdateDestroyView, CurrentUserView,
    ProductTypeListCreateView, ProductTypeRetrieveUpdateDestroyView,
    ProductListCreateView, ProductRetrieveUpdateDestroyView,
    OrderProductListCreateView, OrderProductRetrieveUpdateDestroyView,
    StatusListCreateView, StatusRetrieveUpdateDestroyView,
    OrderListCreateView, OrderRetrieveUpdateDestroyView, ChangeOrderStatusView,LoginView,ChangePasswordView,StaffCreateRetrieveView,StaffUpdateDeleteView,DeleteAllOrdersView
)

urlpatterns = [
    # Role URLs
    path('admin/', admin.site.urls), 
    path('roles/', RoleListCreateView.as_view(), name='role-list-create'),
    path('roles/<int:pk>/', RoleRetrieveUpdateDestroyView.as_view(), name='role-detail'),

    # User URLs
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('me/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('staffs/', StaffCreateRetrieveView.as_view(), name='role-2-users-list'),
    path('staffs/<int:pk>/', StaffUpdateDeleteView.as_view(), name='role-2-users-detail'),
    # Product Type URLs
    path('product-types/', ProductTypeListCreateView.as_view(), name='product-type-list-create'),
    path('product-types/<int:pk>/', ProductTypeRetrieveUpdateDestroyView.as_view(), name='product-type-detail'),

    # Product URLs
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),

    # Order Product URLs
    path('order-products/', OrderProductListCreateView.as_view(), name='order-product-list-create'),
    path('order-products/<int:pk>/', OrderProductRetrieveUpdateDestroyView.as_view(), name='order-product-detail'),

    # Status URLs
    path('statuses/', StatusListCreateView.as_view(), name='status-list-create'),
    path('statuses/<int:pk>/', StatusRetrieveUpdateDestroyView.as_view(), name='status-detail'),

    # Order URLs
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('orders/<int:pk>/change-status/', ChangeOrderStatusView.as_view(), name='order-change-status'),
    path('admin/delete-orders/', DeleteAllOrdersView.as_view(), name='delete_all_orders'),
    path('login/', LoginView.as_view(), name='login'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)