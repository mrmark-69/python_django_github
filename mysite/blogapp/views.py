from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Article


class ArticlesListView(ListView):
    template_name = 'article_list.html'
    context_object_name = 'articles'
    queryset = Article.objects.select_related('author', 'category').prefetch_related('tags').defer('content')
