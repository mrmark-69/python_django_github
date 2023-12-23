from django.contrib import admin

from blogapp.models import Author, Category, Tag, Article

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = "id", "title", "content_short", "pub_date", "author_name", "articles_category", "published"
    list_display_links = "id", "title",
    ordering = "id", "title",
    search_fields = "title", "author", "id"

    def content_short(self, obj: Article) -> str:
        if len(obj.content) > 48:
            return f"{obj.content[:48]}..."
        return obj.content

    def author_name(self, obj: Article) -> str:
        return obj.author.name

    def articles_category(self, obj: Article) -> str:
        return obj.category.name