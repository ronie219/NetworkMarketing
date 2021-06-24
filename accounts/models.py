import uuid
import base64
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from accounts.utils import create_unique_id

GENDER = [("F", 'Female'), ("M", 'Male'), ("0", 'Other')]


class AccountManager(BaseUserManager):

    def create_user(self, email, mobile, password=None):
        if not email:
            raise ValueError("Email is mandatory")
        if not mobile:
            raise ValueError("Mobile number is mandatory")
        user = self.model(
            email=self.normalize_email(email),
            mobile=mobile,
        )
        user.set_password(password)
        parent = Accounts.objects.filter(referral_code=self.parent_id)
        if len(parent) == 1:
            self.parent_id = parent[0].id
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, password=None):
        user = self.create_user(email=self.normalize_email(
            email), password=password, mobile=mobile)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.parent_id = 1
        user.save(using=self._db)
        return user


class Accounts(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    email = models.EmailField(
        verbose_name="Email/Username", max_length=60, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    date_joined = models.DateTimeField(
        verbose_name="Date Login", auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name="Last joined", auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER, max_length=15)
    mobile = models.CharField(max_length=10, unique=True)
    referral_code = models.CharField(max_length=10,unique=True)
    mobile_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    address = models.CharField(max_length=250, null=False, blank=False)
    aadhar_card = models.CharField(max_length=12, unique=True)
    pan_number = models.CharField(max_length=10, unique=True)
    # aadhar_card_image = models.BinaryField(null=False)
    parent_id = models.CharField(unique=False, blank=False, null=False, max_length=250, verbose_name="DS ID")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', ]

    objects = AccountManager()

    class Meta:
        ordering = ["first_name"]
        verbose_name = 'account'
        verbose_name_plural = "accounts"
        db_table = 'users'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse('accounts:payment')

    def generate_referal_code(self):
        id = create_unique_id()
        print(type(id),id)
        while 1:
            if len(Accounts.objects.filter(referral_code=id)) != 0:
                id = create_unique_id()
            else:
                return id

    def activate_user(self):
        self.is_active = True
        self.save()

    def save(self, *args, **kwargs):
        if self.referral_code == '': self.referral_code = self.generate_referal_code()
        parent = Accounts.objects.filter(referral_code=self.parent_id)
        if len(parent) == 1:
            self.parent_id = parent[0].id
        return super(Accounts, self).save(*args, **kwargs)
