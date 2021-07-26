from django.urls import path
from .views import ChangePasswordView, EditProfileView, ClientFormView, LaundryManFormView, login_view,\
     password_success, register_view, edit_profile, EditLaundryProfileView, edit_laundry_profile

urlpatterns = [
    path('login/success/', login_view, name='login_success'),
    path('register/success', register_view, name='register_success'),
    path('edit_profile/<slug>', EditProfileView.as_view(), name='edit_profile'),
    path('save_edit/', edit_profile, name='save_edit'),
    path('edit_laundry_profile/<slug>', EditLaundryProfileView.as_view(), name='edit_laundry_profile'),
    path('save_laundry_edit/', edit_laundry_profile, name='save_laundry_edit'),
    path('password/', ChangePasswordView.as_view(template_name='registration/change-password.html')),
    path('password_updated/', password_success, name='password_updated'),
    path('new/client/', ClientFormView.as_view(), name='new_client'),
    path('new/laundry_man', LaundryManFormView.as_view(), name='new_laundry_man'),
]