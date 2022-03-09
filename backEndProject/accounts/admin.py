from django.contrib import admin

from .models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'first_name', 'last_name', 'age', 'school_year', 'gpa', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)