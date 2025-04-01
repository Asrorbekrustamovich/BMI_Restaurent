from rest_framework import serializers
from .models import Role, User, product_type, Product, OrderProduct, Status, Order
from rest_framework import serializers
from django.contrib.auth import authenticate
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role',
        write_only=True,
        required=False
    )
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'role', 'role_id', 'is_available',
            'shift_start', 'shift_end','password'
        ]
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data.get('password', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            role=validated_data.get('role', None)
        )
        return user

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_type
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    type = ProductTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=product_type.objects.all(),
        source='type',
        write_only=True
    )
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'image', 
            'price', 'type', 'type_id'
        ]

class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = OrderProduct
        fields = [
            'id', 'product', 'product_id', 'quantity',
            'price_at_order', 'subtotal'
        ]

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not authenticate(username=user.username, password=value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderProductSerializer(many=True)
    status = StatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all(),
        source='status',
        write_only=True
    )
    total_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = Order
        fields = [
            'id', 'table_number', 'order_time', 'status',
            'status_id', 'orderitems', 'total_price'
        ]
    
    def create(self, validated_data):
        order_items_data = self.context.get('request').data.get('orderitems', [])
        order = Order.objects.create(
            table_number=validated_data['table_number'],
            status=validated_data['status']
        )
        
        for item_data in order_items_data:
            product = Product.objects.get(pk=item_data['product_id'])
            OrderProduct.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                price_at_order=product.price
            )
        
        return order