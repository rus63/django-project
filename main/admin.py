from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Tag, Task

admin.site.register(User, UserAdmin)


class TaskManagerAdminSite(admin.AdminSite):
    pass


task_manager_admin_site = TaskManagerAdminSite(name="Task manager admin")

@admin.register(Tag, site=task_manager_admin_site)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Task, site=task_manager_admin_site)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(User, site=task_manager_admin_site)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "first_name", "last_name", "is_staff", "is_active", "role"]


