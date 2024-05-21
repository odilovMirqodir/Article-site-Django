from django.contrib import admin
from .models import Article, Category, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'created_at', 'update_at', 'is_published')
    list_display_links = ('pk', 'title')
    list_editable = ('category', 'is_published')
    list_filter = ('category',)
    search_fields = ('title', 'content')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Comment)

