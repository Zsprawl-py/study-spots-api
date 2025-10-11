from django.contrib import admin

from .models import Review, Spot


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "wifi", "outlets", "quiet_level")
    list_display_links = ("name",)
    search_fields = ("name", "address", "city")
    list_filter = ("city", "wifi", "outlets", "quiet_level")
    readonly_fields = ("created_at", "updated_at")
    # prepopulated_fields = {"slug": ("name",)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("spot", "user", "rating", "visit_date", "created_at")
    search_fields = ("spot__name", "user__username", "comment")
    list_filter = ("rating",)
    readonly_fields = ("created_at", "updated_at")
