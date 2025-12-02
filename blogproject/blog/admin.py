from django.contrib import admin

# Register your models here.
from .models import Post, Category

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published", "views", "is_new")
    prepopulated_fields = {"slug": ("title",)}
    
    def is_new(self, obj):
        return obj.published_recently()

    is_new.boolean = True
    is_new.short_description = "Recent?"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    


    