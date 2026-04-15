# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser, CompanyGroup, GroupLicense, ProcessingHistory

# # 1. Customize the User Admin
# class CustomUserAdmin(UserAdmin):
#     # Fieldsets define the layout of the "Edit User" page
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         # Custom Section
#         ('Company Group & Access', {
#             'fields': ('company_group', 'access_rights', 'process_license_limit')
#         }),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )

#     # List Display defines the columns in the "List Users" page
#     list_display = (
#         'username',
#         'email',
#         'first_name',
#         'last_name',
#         'company_group',  # Displays the ForeignKey string representation
#         'access_rights',
#         'is_staff'
#     )
    
#     # Add filters for easier searching
#     list_filter = ('company_group', 'access_rights', 'is_staff', 'is_superuser')
#     search_fields = ('username', 'first_name', 'last_name', 'email', 'company_group__name')

# # 2. Register Models
# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(CompanyGroup)
# admin.site.register(GroupLicense)      # Added this so you can edit licenses manually
# admin.site.register(ProcessingHistory) # Added this so you can view logs

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CompanyGroup, GroupLicense, ProcessingHistory, CreditRequest

# 1. Custom User Admin
class CustomUserAdmin(UserAdmin):
    # Fieldsets define the layout of the "Edit User" page
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        # Custom Section
        ('Company Group & Access', {
            'fields': ('company_group', 'access_rights', 'process_license_limit')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # List Display defines the columns in the "List Users" page
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'company_group',  # Displays the ForeignKey string representation
        'access_rights',
        'is_staff'
    )
    
    # Add filters for easier searching
    list_filter = ('company_group', 'access_rights', 'is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'company_group__name')

# 2. Processing History Admin (With Custom Columns)
class ProcessingHistoryAdmin(admin.ModelAdmin):
    # This enables the specific columns you asked for
    list_display = ('get_group_name', 'get_user_full_name', 'input_filename', 'rows_processed', 'timestamp')
    list_filter = ('group', 'timestamp')
    search_fields = ('group__name', 'user__username', 'user__first_name', 'input_filename')
    readonly_fields = ('timestamp',) # Prevent accidental editing of logs

    # Helper to show Group Name
    @admin.display(description='Group Name', ordering='group__name')
    def get_group_name(self, obj):
        return obj.group.name

    # Helper to show User's Full Name
    @admin.display(description="User's Full Name", ordering='user__first_name')
    def get_user_full_name(self, obj):
        if obj.user:
            # Returns "John Doe" if available, otherwise "jdoe123"
            return obj.user.get_full_name() or obj.user.username
        return "System/Deleted User"

# 3. Credit Request Admin
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ('group', 'requested_rows', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('group__name',)
    list_editable = ('status',) # Allows you to Approve/Reject directly from the list view

# 4. Group License Admin
class GroupLicenseAdmin(admin.ModelAdmin):
    list_display = ('group', 'row_limit', 'expiry_date', 'is_active')
    list_filter = ('is_active',)

# 5. Register Models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CompanyGroup)
admin.site.register(GroupLicense, GroupLicenseAdmin)
admin.site.register(ProcessingHistory, ProcessingHistoryAdmin)
admin.site.register(CreditRequest, CreditRequestAdmin) 