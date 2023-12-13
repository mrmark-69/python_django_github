from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView

from blogapp.models import Article


class ArticlesListView(ListView):
    template_name = 'blogapp/articles_list.html'
    context_object_name = 'articles'
    queryset = (Article.objects.filter(published=True).select_related('author', 'category').
                prefetch_related('tags').defer('content').order_by("-pub_date"))


class ArticleDetailView(DetailView):
    model = Article


class LatestArticlesFeed(Feed):
    title = 'Blog articles (latest)'
    description = 'Updates on changes and addition blog articles'
    link = reverse_lazy("blogapp:articles")

    def items(self):
        return (Article.objects.filter(published=True).select_related('author', 'category').
                prefetch_related('tags').defer('content').order_by("-pub_date"))

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.content[:200]
