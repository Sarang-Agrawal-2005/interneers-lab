from django.contrib import admin
from django.urls import path
from django.http import HttpResponse, JsonResponse

def hello_world(request):
    name = request.GET.get("name")

    if name:
        return JsonResponse({"message" : f"Hello {name}"})
    else:
        return JsonResponse({"message" : "Hello World"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_world),
]
