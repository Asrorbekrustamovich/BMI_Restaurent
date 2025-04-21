from rest_framework import generics, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Role, User, product_type, Product, OrderProduct, Status, Order
from .serializers import (
    RoleSerializer, UserSerializer, ProductTypeSerializer,
    ProductSerializer, OrderProductSerializer, StatusSerializer, OrderSerializer
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import PasswordChangeSerializer
from django.contrib.auth import update_session_auth_hash
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from app.models import Role
from app.serializers import UserSerializer
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]

class RoleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAdminUser,IsAuthenticated]

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all().select_related('role')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all().select_related('role')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,IsAdminUser ]


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Update session to prevent logout
            update_session_auth_hash(request, user)
            
            return Response({"status": "password changed"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductTypeListCreateView(generics.ListCreateAPIView):
    queryset = product_type.objects.all()
    serializer_class = ProductTypeSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            # Allow authenticated users who are either admins or staff
            return [IsAuthenticated()]
        elif self.request.method == 'POST':
            # Only allow admins to create
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()

class ProductTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = product_type.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated,IsAdminUser   ]
User = get_user_model()

class StaffCreateRetrieveView(generics.ListCreateAPIView):
    queryset = User.objects.filter(role__id=2)
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Admins can create staff users (POST)
        Any authenticated user can view staff list (GET)
        """
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        """Automatically sets role=2 and handles password hashing"""
        role = Role.objects.get(id=2)
        password = serializer.validated_data.get('password')
        user = serializer.save(role=role, is_staff=True)
        if password:
            user.set_password(password)
            user.save()

class StaffUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role__id=2)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        """Maintains role=2 and handles password hashing"""
        password = serializer.validated_data.get('password')
        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().select_related('type')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]  # Only admins can create
        return [AllowAny()]  # Anyone can view

    def get_queryset(self):
        queryset = super().get_queryset()
        product_type = self.request.query_params.get('type')
        if product_type:
            queryset = queryset.filter(type_id=product_type)
        return queryset


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().select_related('type')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

class OrderProductListCreateView(generics.ListCreateAPIView):
    queryset = OrderProduct.objects.all().select_related('product')
    serializer_class = OrderProductSerializer

class OrderProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderProduct.objects.all().select_related('product')
    serializer_class = OrderProductSerializer

class StatusListCreateView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]

class StatusRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthenticated]

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all().select_related('status').prefetch_related(
        'orderitems', 'orderitems__product'
    ).order_by('-id')
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        table_number = self.request.query_params.get('table')
        status_id = self.request.query_params.get('status')
        
        if table_number:
            queryset = queryset.filter(table_number=table_number)
        if status_id:
            queryset = queryset.filter(status_id=status_id)
            
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # First create the order
        order = Order.objects.create(
            table_number=serializer.validated_data['table_number'],
            status=serializer.validated_data['status']
        )
        
        # Then create and associate order items
        order_items = []
        for item_data in request.data.get('orderitems', []):
            product = get_object_or_404(Product, pk=item_data['product_id'])
            order_item = OrderProduct.objects.create(
                product=product,
                quantity=item_data['quantity'],
                price_at_order=product.price
            )
            order_items.append(order_item)
        
        # Add items to order using many-to-many relationship
        order.orderitems.add(*order_items)
        
        # Return the complete order data
        return Response(
            OrderSerializer(order, context=self.get_serializer_context()).data,
            status=status.HTTP_201_CREATED
        )

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all().select_related('status').prefetch_related(
        'orderitems', 'orderitems__product'
    )
    serializer_class = OrderSerializer

class ChangeOrderStatusView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        new_status_id = request.data.get('status_id')
        
        if not new_status_id:
            return Response(
                {'error': 'status_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            new_status = Status.objects.get(pk=new_status_id)
        except status.DoesNotExist:
            return Response(
                {'error': 'Invalid status_id'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = new_status
        order.save()
        return Response(self.get_serializer(order).data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)  # Get default token
        
        # Add custom claims (role_id will be in the access token)
        # token['user_id'] = user.id
        token['role_id'] = user.role.id if user.role else None
        
        return token
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

from .permissions import IsStaff  # Make sure you have this import

class Status1OrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Added IsStaff permission
    
    def get_queryset(self):
        return Order.objects.filter(status_id=1).select_related('status').prefetch_related(
            'orderitems', 'orderitems__product'
        ).order_by('-id')

class Status2OrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Added IsStaff permission
    
    def get_queryset(self):
        return Order.objects.filter(status_id=2).select_related('status').prefetch_related(
            'orderitems', 'orderitems__product'
        ).order_by('-id')

class Status3OrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Added IsStaff permission
    
    def get_queryset(self):
        return Order.objects.filter(status_id=3).select_related('status').prefetch_related(
            'orderitems', 'orderitems__product'
        ).order_by('-id')
    
class DeleteAllOrdersView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        Order.objects.all().delete()
        OrderProduct.objects.all().delete()
        return Response({"detail": "All orders and order products have been deleted."}, status=status.HTTP_200_OK)