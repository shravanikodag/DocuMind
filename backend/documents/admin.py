from django.contrib import admin
from .models import Document, DocumentChunk


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "uploaded_at")
    list_filter = ("status",)
    search_fields = ("title",)


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ("document", "chunk_index", "page_number")
    list_filter = ("document",)
    search_fields = ("content",)
 

# Register your models here.
