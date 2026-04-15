from django import forms
from django.contrib.auth import get_user_model
from .models import CompanyGroup 
# Removed Company, Department imports since they are deleted

# Get the active User model
User = get_user_model()

class CustomUserForm(forms.ModelForm):
    # We define password fields manually to control the UI and validation
    password = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    password2 = forms.CharField(
        label="Confirm Password", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = User
        # --- UPDATED: Removed 'companies' and 'departments' ---
        fields = ("username", "first_name", "last_name", "email", "company_group", "access_rights")
    
    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling to all fields
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                existing_class = field.widget.attrs.get('class', '')
                field.widget.attrs.update({'class': existing_class + ' form-control'})

        if not self.request_user:
            return

        # --- LOGIC FOR SUPERUSER ---
        if self.request_user.is_superuser:
            # Superuser can see and select any Group
            self.fields['company_group'].queryset = CompanyGroup.objects.all()
        
        # --- LOGIC FOR GROUP ADMIN ---
        elif self.request_user.access_rights == 'admin':
            # 1. Get the admin's single group
            admin_group = self.request_user.company_group

            if admin_group:
                # 2. Lock 'company_group' field to their own group
                # We filter by ID so the dropdown only shows their group
                self.fields['company_group'].queryset = CompanyGroup.objects.filter(id=admin_group.id)
                self.fields['company_group'].initial = admin_group
                # Optional: Make it visually indicated as read-only (HTML readonly attribute handled in template or here)
                # Note: 'readonly' doesn't always prevent POST modification, filtering queryset above ensures security.
                self.fields['company_group'].widget.attrs['readonly'] = True
            else:
                # If admin has no group (edge case), show nothing
                self.fields['company_group'].queryset = CompanyGroup.objects.none()

    def clean(self):
        """
        Verify that passwords match.
        """
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error('password2', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        """
        Save the user and set the password correctly.
        """
        user = super().save(commit=False)
        p1 = self.cleaned_data.get("password")
        if p1:
            user.set_password(p1)
        if commit:
            user.save()
            # self.save_m2m() is not strictly needed anymore for custom fields 
            # since companies/departments are gone, but good practice to keep 
            # if you use standard django groups later.
            self.save_m2m() 
        return user


# --- Form for Company Group ---
class CompanyGroupForm(forms.ModelForm):
    class Meta:
        model = CompanyGroup
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Group Name'}),
        }