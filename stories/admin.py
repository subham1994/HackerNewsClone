from django.contrib import admin
from .models import Story


class StoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'domain', 'moderator', 'points', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('title',)

    fieldsets = [
        ('Story', {'fields': ('title', 'url', 'points')}),
        ('Moderator', {'fields': ('moderator',)}),
        ('Change history', {'fields': ('created_at', 'updated_at')})
    ]

    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Story, StoryAdmin)
