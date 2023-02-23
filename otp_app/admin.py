from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from otp_app.forms import CustomUserChangeForm, CustomUserCreationForm
# Register your models here.

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username','email','is_staff']
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (
            "None", {
                "fields":("otp_verified","otp_enabled","otp_base32",'otp_auth_url',),
            }
        ),
    )
    add_fieldsets = (
        (
            "Create User", {
                "classes":("wide",),
                "fields":('username','email','password1','password2'),
            }
        ),
    )
