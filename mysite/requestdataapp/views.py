from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import UserBioForm, UploadFileForm


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b

    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm()
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        # Проверка на заполненность формы данными.
        if form.is_valid():
            myfile = form.cleaned_data["file"]
            fs = FileSystemStorage()
            # Сохраняем файл
            filename = fs.save(myfile.name, myfile)
            # Выводим сообщение о сохранении файла.
            return render(request, "requestdataapp/file-upload.html",
                              {"message": f"File '{filename}' uploaded successfully.", "form": form})
    else:
        form = UploadFileForm()

    return render(request, "requestdataapp/file-upload.html", {"form": form})
