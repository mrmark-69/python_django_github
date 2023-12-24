from django.urls import path

from .views import ArticlesListView, ArticleDetailView, LatestArticlesFeed

app_name = 'blogapp'

urlpatterns = [
    path('articles/', view=ArticlesListView.as_view(), name='articles'),
    path('article/<int:pk>', view=ArticleDetailView.as_view(), name='article'),
    path('articles/latest/feed/', LatestArticlesFeed(), name="articles-feed"),
]
