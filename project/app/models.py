# import auto_prefetch
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.conf import settings
# import json

# ROLE_CHOICES = (
#     ('download', 'Download'),
#     ('hod', 'HOD'),
#     ('admin', 'Group Admin'),
# )

# class CompanyGroup(auto_prefetch.Model):
#     name = models.CharField(max_length=150, unique=True)
#     created_by = auto_prefetch.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         null=True, blank=True,
#         on_delete=models.SET_NULL,
#         related_name='created_groups'
#     )

#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Company Group"

#     def __str__(self):
#         return self.name


# class Company(auto_prefetch.Model):
#     name = models.CharField(max_length=100)
#     group = auto_prefetch.ForeignKey(
#         CompanyGroup,
#         on_delete=models.CASCADE,
#         related_name='companies'
#     )

#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Company"

#     def __str__(self):
#         return self.name


# class Department(auto_prefetch.Model):
#     name = models.CharField(max_length=100)
#     company = auto_prefetch.ForeignKey(
#         Company,
#         on_delete=models.CASCADE,
#         related_name='departments'
#     )

#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Department"

#     def __str__(self):
#         return self.name


# class CustomUser(AbstractUser, auto_prefetch.Model):
#     groups = models.ManyToManyField(CompanyGroup, blank=True, related_name="users")
#     companies = models.ManyToManyField(Company, blank=True)
#     departments = models.ManyToManyField(Department, blank=True)
#     access_rights = models.CharField(
#         max_length=10,
#         choices=ROLE_CHOICES,
#         default='download',
#         verbose_name='Access Rights'
#     )
    
#     # --- ADDED: Process License Limit ---
#     process_license_limit = models.IntegerField(
#         default=5, 
#         verbose_name="Process License Limit",
#         help_text="Number of processes allowed. -1 indicates unlimited."
#     )

#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Custom User"

#     def save(self, *args, **kwargs):
#         """
#         Override save to set license limits on creation.
#         """
#         if not self.pk:  # Check if this is a new instance (creation)
#             if self.is_superuser:
#                 self.process_license_limit = -1  # Unlimited for SuperUser
#             else:
#                 self.process_license_limit = 5   # 5 for regular demo users
        
#         super().save(*args, **kwargs)


# # --- NEW MODELS FOR RECONCILIATION MIGRATION ---

# class GroupLicense(auto_prefetch.Model):
#     """
#     Replaces the offline Keybase license. 
#     Controls access per CompanyGroup.
#     """
#     group = auto_prefetch.OneToOneField(
#         CompanyGroup, 
#         on_delete=models.CASCADE, 
#         related_name='license'
#     )
#     is_active = models.BooleanField(default=True)
#     expiry_date = models.DateField()
#     # "Allowed row count / plan restrictions"
#     row_limit = models.BigIntegerField(default=10000000, help_text="Total rows allowed to be processed")
    
#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Group License"

#     def __str__(self):
#         return f"License for {self.group.name}"


# class ProcessingHistory(auto_prefetch.Model):
#     """
#     Stores history in DB instead of local JSON/encrypted files.
#     """
#     group = auto_prefetch.ForeignKey(
#         CompanyGroup, 
#         on_delete=models.CASCADE, 
#         related_name='processing_history'
#     )
#     user = auto_prefetch.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='processing_history'
#     )
#     # Stores "file1_name | file2_name"
#     input_filename = models.CharField(max_length=500) 
#     rows_processed = models.IntegerField(default=0)
#     # "Combined unique key: filename + rows"
#     unique_key = models.CharField(max_length=500, db_index=True)
#     metadata = models.JSONField(default=dict, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Processing Run"
#         ordering = ['-timestamp']

#     def __str__(self):
#         return f"{self.input_filename} ({self.timestamp})"



# import auto_prefetch
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.conf import settings
# import json

# ROLE_CHOICES = (
#     ('download', 'Download'),
#     ('hod', 'HOD'),
#     ('admin', 'Group Admin'),
# )

# class CompanyGroup(auto_prefetch.Model):
#     name = models.CharField(max_length=150, unique=True)
#     created_by = auto_prefetch.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         null=True, blank=True,
#         on_delete=models.SET_NULL,
#         related_name='created_groups'
#     )

#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Company Group"

#     def __str__(self):
#         return self.name


# class Company(auto_prefetch.Model):
#     name = models.CharField(max_length=100)
#     # 

#     group = auto_prefetch.ForeignKey(
#         CompanyGroup,
#         on_delete=models.CASCADE,
#         related_name='companies'
#     )

#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Company"

#     def __str__(self):
#         return self.name


# class Department(auto_prefetch.Model):
#     name = models.CharField(max_length=100)
#     company = auto_prefetch.ForeignKey(
#         Company,
#         on_delete=models.CASCADE,
#         related_name='departments'
#     )

#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Department"

#     def __str__(self):
#         return self.name


# class CustomUser(AbstractUser, auto_prefetch.Model):
#     # --- CHANGED: ManyToMany -> ForeignKey ---
#     # This enforces "One User = One Group"
#     company_group = auto_prefetch.ForeignKey(
#         CompanyGroup, 
#         on_delete=models.SET_NULL, # If group is deleted, user stays but has no group
#         null=True, 
#         blank=True, 
#         related_name="users",
#         verbose_name="Company Group"
#     )
    
#     # Note: I removed the field named 'groups'. 
#     # AbstractUser already has a field named 'groups' for Django Permissions.
#     # We use 'company_group' to avoid conflict and be specific.

#     companies = models.ManyToManyField(Company, blank=True)
#     departments = models.ManyToManyField(Department, blank=True)
    
#     access_rights = models.CharField(
#         max_length=10,
#         choices=ROLE_CHOICES,
#         default='download',
#         verbose_name='Access Rights'
#     )
    
#     process_license_limit = models.IntegerField(
#         default=5, 
#         verbose_name="Process License Limit",
#         help_text="Number of processes allowed. -1 indicates unlimited."
#     )

#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Custom User"

#     def save(self, *args, **kwargs):
#         """
#         Override save to set license limits on creation.
#         """
#         if not self.pk:  # Check if this is a new instance (creation)
#             if self.is_superuser:
#                 self.process_license_limit = -1  # Unlimited for SuperUser
#             else:
#                 self.process_license_limit = 5   # 5 for regular demo users
        
#         super().save(*args, **kwargs)

#     @property
#     def is_group_admin(self):
#         """Helper to check if user is the admin/creator of their group"""
#         if self.company_group and self.company_group.created_by == self:
#             return True
#         return self.access_rights == 'admin'


# # --- RECONCILIATION MODELS ---

# class GroupLicense(auto_prefetch.Model):
#     group = auto_prefetch.OneToOneField(
#         CompanyGroup, 
#         on_delete=models.CASCADE, 
#         related_name='license'
#     )
#     is_active = models.BooleanField(default=True)
#     expiry_date = models.DateField()
#     row_limit = models.BigIntegerField(default=10000000, help_text="Total rows allowed to be processed")
    
#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Group License"

#     def __str__(self):
#         return f"License for {self.group.name}"


# class ProcessingHistory(auto_prefetch.Model):
#     group = auto_prefetch.ForeignKey(
#         CompanyGroup, 
#         on_delete=models.CASCADE, 
#         related_name='processing_history'
#     )
#     user = auto_prefetch.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='processing_history'
#     )
#     input_filename = models.CharField(max_length=500) 
#     rows_processed = models.IntegerField(default=0)
#     unique_key = models.CharField(max_length=500, db_index=True)
#     metadata = models.JSONField(default=dict, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Processing Run"
#         ordering = ['-timestamp']

#     def __str__(self):
#         return f"{self.input_filename} ({self.timestamp})"

import auto_prefetch
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
import json


ROLE_CHOICES = (
    ('download', 'Download'),
    ('hod', 'HOD'),
    ('admin', 'Group Admin'),
)

class CompanyGroup(auto_prefetch.Model):
    name = models.CharField(max_length=150, unique=True)
    created_by = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='created_groups'
    )

    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "Company Group"

    def __str__(self):
        return self.name

# --- REMOVED COMPANY AND DEPARTMENT MODELS ---

class CustomUser(AbstractUser, auto_prefetch.Model):
    # --- FK: Ensures 1 User = 1 Group ---
    company_group = auto_prefetch.ForeignKey(
        CompanyGroup, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="users",
        verbose_name="Company Group"
    )
    
    # --- REMOVED: companies and departments ManyToMany fields ---
    
    access_rights = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='download',
        verbose_name='Access Rights'
    )
    
    # This is the limit per USER (optional, if you still want user-level limits)
    process_license_limit = models.IntegerField(
        default=5, 
        verbose_name="Process License Limit",
        help_text="Number of processes allowed. -1 indicates unlimited."
    )

    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "Custom User"

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.is_superuser:
                self.process_license_limit = -1
            else:
                self.process_license_limit = 5
        super().save(*args, **kwargs)

    @property
    def is_group_admin(self):
        if self.company_group and self.company_group.created_by == self:
            return True
        return self.access_rights == 'admin'


# --- LICENSE MODELS ---

class GroupLicense(auto_prefetch.Model):
    group = auto_prefetch.OneToOneField(
        CompanyGroup, 
        on_delete=models.CASCADE, 
        related_name='license'
    )
    is_active = models.BooleanField(default=True)
    expiry_date = models.DateField()
    # "5 Credit" logic applied here
    row_limit = models.BigIntegerField(default=5, help_text="Total credits/rows allowed")

    # --- ADD THESE TWO LINES ---
    is_row_based = models.BooleanField(default=False)
    is_file_based = models.BooleanField(default=True)
    rows_per_credit = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text="Number of rows that count as 1 credit. Empty for File Based."
    )
    # ---------------------------
    
    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "Group License"

    def __str__(self):
        return f"License for {self.group.name}"


# class ProcessingHistory(auto_prefetch.Model):
#     group = auto_prefetch.ForeignKey(
#         CompanyGroup, 
#         on_delete=models.CASCADE, 
#         related_name='processing_history'
#     )
#     user = auto_prefetch.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='processing_history'
#     )
#     input_filename = models.CharField(max_length=500) 
#     rows_processed = models.IntegerField(default=0)
#     unique_key = models.CharField(max_length=500, db_index=True)
#     metadata = models.JSONField(default=dict, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta(auto_prefetch.Model.Meta):
#         verbose_name = "Processing Run"
#         ordering = ['-timestamp']

#     def __str__(self):
#         return f"{self.input_filename} ({self.timestamp})"


# ==========================================
# SIGNAL TO AUTO-ACTIVATE LICENSE
# ==========================================
class ProcessingHistory(auto_prefetch.Model):
    group = auto_prefetch.ForeignKey(
        CompanyGroup, 
        on_delete=models.CASCADE, 
        related_name='processing_history'
    )
    user = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='processing_history'
    )
    input_filename = models.CharField(max_length=500) 
    rows_processed = models.IntegerField(default=0)
    unique_key = models.CharField(max_length=500, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta(auto_prefetch.Model.Meta):
        verbose_name = "Processing Run"
        ordering = ['-timestamp']

    def __str__(self):
        # 1. Get the Group Name
        group_name = self.group.name
        
        # 2. Get User Full Name (Safe Handling)
        if self.user:
            # Try to get full name; if empty, fall back to username
            user_full_name = self.user.get_full_name() or self.user.username
        else:
            user_full_name = "System/Deleted User"

        # 3. Return the formatted string
        return f"{group_name} | {user_full_name} | {self.input_filename}"



@receiver(post_save, sender=CompanyGroup)
def create_group_license(sender, instance, created, **kwargs):
    """
    Automatically creates a license when a new CompanyGroup is created.
    Settings: Active=True, Expiry=Next Month, Credits=5.
    """
    if created:
        # Calculate expiry date (30 days from now)
        next_month = timezone.now().date() + timedelta(days=30)
        
        
        
        GroupLicense.objects.create(
            group=instance,
            is_active=True,       # Activate immediately
            expiry_date=next_month, # Set to next month
            row_limit=5           # Give 5 credits
        )

# models.py

class CreditRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    group = models.ForeignKey(CompanyGroup, on_delete=models.CASCADE)
    requested_rows = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.group.name} - {self.requested_rows} rows ({self.status})"