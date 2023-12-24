from django.contrib import admin

from models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = "id", "user", "user_verbose", "bio_short", "agreement_accepted",
    # readonly_fields = "user",
    list_display_links = "id", "user",
    ordering = "id", "user",
    search_fields = "id", "user__username"
    fieldsets = [
        (None, {
            "fields": ("user", "bio"),
        }),
        ("Avatar options", {
            "fields": ("avatar",),
            # "classes": ("collapse", "wide"),
        }),
        ("Agreement options", {"fields": ("agreement_accepted",),
                               "classes": ("collapse",),
                               "description": "Agreement options. Field 'agreement_accepted' is for accept agreement.",
                               }),
    ]

    def bio_short(self, obj: Profile) -> str:
        if len(obj.bio) > 48:
            return f"{obj.bio[:48]}..."
        return obj.bio

    def user_verbose(self, obj: Profile) -> str:
        return obj.user.first_name or obj.user.username
