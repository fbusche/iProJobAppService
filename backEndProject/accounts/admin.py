from django.contrib import admin

from .models import User, Label

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'first_name', 'last_name', 'age', 'school_year', 'gpa', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('email', 'first_name', 'last_name')

class LabelAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'id')

admin.site.register(User, UserAdmin)
admin.site.register(Label, LabelAdmin)