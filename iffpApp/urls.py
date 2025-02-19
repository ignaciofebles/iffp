from django.urls import path
from iffpApp import views
from django.conf import settings
from django.conf.urls.static import static
from .views import politica_cookies

urlpatterns = [
    path('', views.home, name="Home"),    
    path("politica-de-cookies/", politica_cookies, name="politica_cookies"),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


