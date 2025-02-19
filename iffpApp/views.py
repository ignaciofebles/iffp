from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'iffpApp/home.html')


def politica_cookies(request):
    return render(request, "iffpApp/politica_cookies.html")
