from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_migrate)
def create_admin_user(sender, **kwargs):
    # Fix: Ensure this runs only for the app containing CustomUser
    # Checking sender.name == 'app' fails if the app is named differently (e.g., 'users', 'core')
    try:
        # Check if the CustomUser model belongs to this app configuration
        sender.get_model('CustomUser')
    except LookupError:
        return  # This signal is running for a different app; skip it.

    from .models import CustomUser, CompanyGroup, GroupLicense
    
    # Check if any users exist
    if not CustomUser.objects.exists():
        print("No users found. Creating default Super Admin and Group...")

        # 1. Create the default Superuser
        user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword', # Change this in production
            first_name='Admin',
            last_name='User',
            access_rights='admin'
        )

        # 2. Create the "Default Group"
        # NOTE: The 'post_save' signal in models.py will AUTOMATICALLY 
        # create a GroupLicense with 5 credits and 30 days expiry.
        admin_group = CompanyGroup.objects.create(
            name="Default Group", 
            created_by=user
        )

        # 3. Assign User to Group (ForeignKey)
        user.company_group = admin_group
        user.save()

        # 4. UPGRADE the License for the Admin Group
        # Since the signal already created a default "Demo License", 
        # we just fetch it and upgrade it to "Unlimited/Long-term".
        try:
            license = admin_group.license
            license.expiry_date = timezone.now().date() + timedelta(days=3650) # 10 Years
            license.row_limit = 1000000000 # High limit
            license.save()
            print(" > Auto-generated license upgraded to Admin License.")
        except ObjectDoesNotExist:
            print(" > Warning: License not found for admin group.")

        print("Default admin user and group created successfully.")