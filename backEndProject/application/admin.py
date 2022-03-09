from django.contrib import admin

from .models import Application, Status

# Register your models here.

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'company', 'position', 'location', 'status', 'date_created', 'last_updated', 'job_post',)
    list_filter = ('applicant', 'company', 'location',)
    search_fields = ('company', 'position')
    ordering = ('date_created', 'last_updated')

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_default', 'created_by')
    list_filter = ('created_by', 'is_default')



admin.site.register(Application, ApplicationAdmin)
admin.site.register(Status, StatusAdmin)