from django.contrib import admin
from .models import Category, Institution, Donation
from .models import CustomUser

admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)


class CustomUserAdmin(admin.ModelAdmin):
    exclude = ['password']
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_superuser',)
    readonly_fields = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)