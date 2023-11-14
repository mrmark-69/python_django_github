from django.urls import path

from blogapp.views import ArticlesListView

app_name = 'blogapp'

urlpatterns = [
    path('articles/', view=ArticlesListView.as_view(), name='articles'),
]
