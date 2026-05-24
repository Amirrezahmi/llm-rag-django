from django.contrib import admin
from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_indexed', 'created_at', 'updated_at')
    list_filter = ('is_indexed',)
    search_fields = ('title', 'content')
    readonly_fields = ('content', 'is_indexed', 'created_at', 'updated_at')
