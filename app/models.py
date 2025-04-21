from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')

        user = self.model(username=username, **extra_fields)  # No email field
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        # Get or create Admin role
        admin_role, _ = Role.objects.get_or_create(name='Admin')
        extra_fields.setdefault('role', admin_role)

        return self.create_user(username, password, **extra_fields)


    
class User(AbstractUser):
    groups = None
    user_permissions = None
    
    phone = models.CharField(max_length=20, blank=True, null=True)  # Optional phone number
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='users',
        blank=False,  # Role is required
        null=False
    )
    is_available = models.BooleanField(default=True)
    shift_start = models.TimeField(blank=True, null=True)
    shift_end = models.TimeField(blank=True, null=True)
    
    objects = UserManager()

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role.name if self.role else 'No Role'})"
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'



class product_type(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(product_type, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    price_at_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    
    def save(self, *args, **kwargs):
        if not self.price_at_order:
            self.price_at_order = self.product.price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    @property
    def subtotal(self):
        return self.price_at_order * self.quantity
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Order Product'
        verbose_name_plural = 'Order Products'

class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'

class Order(models.Model):
    orderitems = models.ManyToManyField(OrderProduct, related_name='orders')
    table_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    order_time = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    
    def __str__(self):
        return f"{self.table_number}-{self.status.name}-{self.order_time.strftime('%Y-%m-%d %H:%M:%S')}-{self.id}"
    
    @property
    def total_price(self):
        return sum(item.subtotal for item in self.orderitems.all())
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'