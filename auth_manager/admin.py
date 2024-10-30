from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class AdminUser(UserAdmin):

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or 'change' in request.path:
            return qs
        elif request.user.organization:
            return qs.filter(organization=request.user.organization)
        else:
            return qs.none()

    list_display = ["email", "first_name", "last_name", "is_staff", "is_superuser", "is_active",
                    "created"]
    list_filter = ('is_active', 'email')
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password",
                    'gender',
                    'is_active',
                    'groups',
                    'is_staff',
                )
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(CustomUser, AdminUser)
