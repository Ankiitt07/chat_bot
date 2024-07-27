from django.db import models
from django_tenants.models import DomainMixin, TenantMixin
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.conf import settings

# Create your models here.

status_choice = [
    (0, 'Inactive'),
    (1, 'Active')
]


class WhitelabelDomains(DomainMixin):
    subsription_types = [
        ("97", "97"),
        ("297", "297"),
    ]

    activate = models.BooleanField(default=False)

    tenant = models.OneToOneField(
        settings.TENANT_MODEL,
        db_index=True,
        related_name="whitlable_admin",
        on_delete=models.CASCADE,
    )
    legal_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    subsription_type = models.CharField(
        max_length=30, choices=subsription_types, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)


class Agency(TenantMixin):
    company_name = models.CharField(max_length=100, unique=True)
    domain = models.ForeignKey(
        WhitelabelDomains,
        on_delete=models.CASCADE,
        related_name="agency_whitelable",
        null=True,
        blank=True,
    )
    credit = models.DecimalField(max_digits=30, decimal_places=4, default=100.0000)
    is_suspended = models.BooleanField(default=False)
    auto_create_schema = True
    credit_price = models.DecimalField(max_digits=30, decimal_places=4, default=10.0000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name

    class Meta:
        ordering = ("-created_at",)


class CustomUsers(AbstractBaseUser, PermissionsMixin):

    groups = None
    user_permissions = None
    last_login = None

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    user_status = models.IntegerField(
        choices=status_choice,
        default=1
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
            return self.email

    class Meta:
        db_table = 'custom_user_table'
        managed = True