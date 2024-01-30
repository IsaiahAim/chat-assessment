from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.forms import CustomUserChangeForm, CustomUserCreationForm


# @admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'profile_code', 'gender',
                    'user_type', 'is_active', 'is_staff', 'is_superuser')
    readonly_fields = ("id", 'profile_code', 'created_on', 'updated_on')
    search_fields = ['gender', 'profile_code']
    ordering = ('email',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "id",
                    "profile_code",
                    "first_name",
                    "last_name",
                    "phone_no",
                    "email",
                    "password1",
                    "password2",
                    "gender",
                    "address",
                    "city",
                    "state",
                    "country",
                    "profile_picture",
                    "user_type",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                    "created_on",
                    "updated_on"
                ),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "id",
                    "profile_code",
                    "first_name",
                    "last_name",
                    "phone_no",
                    "email",
                    "password",
                    "gender",
                    "address",
                    "city",
                    "state",
                    "country",
                    "profile_picture",
                    "user_type",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                    "created_on",
                    "updated_on"
                ),
            },
        ),
    )
