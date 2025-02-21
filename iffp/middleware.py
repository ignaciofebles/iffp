from django.shortcuts import redirect
from django.urls import reverse_lazy

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_urls = [
            reverse_lazy('loguear'), 
            reverse_lazy('Autenticacion'), 
            reverse_lazy('politica_cookies')
        ]  # Añade las URLs que quieras permitir sin redirección
        
        if not request.user.is_authenticated and request.path not in allowed_urls:
            return redirect('loguear')
        return self.get_response(request)


