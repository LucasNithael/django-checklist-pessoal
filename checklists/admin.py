from django.contrib import admin
from .models import Area, ChecklistItem

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created_at")
    search_fields = ("name", "user__username")
    list_filter = ("created_at",)

@admin.register(ChecklistItem)
class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "area", "done", "created_at")
    search_fields = ("title", "area__name", "area__user__username")
    list_filter = ("done", "created_at")
