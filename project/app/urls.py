from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # --- Existing Dashboard & Auth Routes ---
    path('', views.dashboard, name='dashboard'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
   
    path('add-user/', views.add_user, name='add_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update-user/<int:user_id>/', views.update_user, name='update_user'),
    path('change-password/', views.change_password, name='change_password'),
   
    #path('company-hierarchy/', views.manage_hierarchy, name='manage_hierarchy'),
    
    # A single URL for all edit operations
    #path('hierarchy/edit/<str:item_type>/<int:item_id>/', views.edit_hierarchy_item, name='edit_hierarchy_item'),
    
    # A single URL for all delete operations
    #path('hierarchy/delete/<str:item_type>/<int:item_id>/', views.delete_hierarchy_item, name='delete_hierarchy_item'),

    path('signup/', views.signup, name='signup'),                        # Signup form
    path('signup/verify-otp/', views.signup_verify_otp, name='signup_verify_otp'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

    # --- NEW: Reconciliation & License System Routes ---
    
    # 1. License Page
    path('license/', views.license_view, name='license_view'),
    
    # 2. Download History
    path('license/download_history/', views.download_history, name='download_history'),

    # 3. Processing Endpoints (FIXED: Added trailing slashes)
    path('upload_files/', views.upload_files, name='upload_files'),
    path('process_data/', views.process_data, name='process_data'),
    path('process_reco/', views.process_reco, name='process_reco'),


    path('super-admin/license-manager/', views.license_manager_view, name='license_manager'),

    path('tools/pdf-to-excel/', views.pdf_to_excel_view, name='pdf_to_excel'),

    path('download_license_report/', views.download_license_report, name='download_license_report'),
]