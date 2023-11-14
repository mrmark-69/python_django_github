from django.shortcuts import render
from django.views.generic import ListView

from blogapp.models import Article


class ArticleListView(ListView):
    template_name = 'article_list.html'
    context_object_name = 'articles'
    queryset = Article.objects.all()