from django.urls import path
from .views import process_get_weiv, user_form, handle_file_upload

app_name = 'requestdataapp'

urlpatterns = [
    path("get/", process_get_weiv, name="get-view"),
    path("bio/", user_form, name="user-form"),
    path("upload/", handle_file_upload, name="file-upload"),
]
