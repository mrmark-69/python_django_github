from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


# Create your views here.
def process_get_weiv(request: HttpRequest) -> HttpResponse:
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
    return render(request, "requestdataapp/user-bio-form.html")


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        # Проверка размера загружаемого файла.
        if myfile.size > 2.62144e6:
            # Если размер превышен, выводится сообщение с предупреждением.
            return render(request, "requestdataapp/file-upload.html",
                          {"message": "Failed to load. File size exceeded 2.5 mb"})
        else:
            # Сохраняем файл
            filename = fs.save(myfile.name, myfile)
            # Выводим сообщение о сохранении файла.
            return render(request, "requestdataapp/file-upload.html",
                          {"message": f"File '{filename}' uploaded successfully."})
    return render(request, "requestdataapp/file-upload.html")
