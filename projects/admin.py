from django.contrib import admin
from .models import SubProject, UserProfile


@admin.register(SubProject)
class SubProjectAdmin(admin.ModelAdmin):
    list_display = ['project_number', 'sub_project', 'construction_unit', 'start_date', 'completion_date', 'created_at']
    list_filter = ['start_date', 'completion_date', 'created_at']
    search_fields = ['project_number', 'sub_project', 'main_construction_unit', 'construction_unit', 'address']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('parent_id', 'main_project', 'main_project_address', 'sub_project')
        }),
        ('详细信息', {
            'fields': ('rectification_details', 'inspection_details')
        }),
        ('可修改信息', {
            'fields': (
                'project_number', 'date', 'construction_period', 
                'start_date', 'completion_date', 'address',
                'construction_unit', 'contact_person', 'phone',
                'contractor', 'contractor_contact', 'owner',
                'area', 'construction_cost', 'on_site_records', 'remarks'
            )
        }),
        ('系统信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_admin', 'organization', 'created_at']
    list_filter = ['is_admin', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'organization'] 