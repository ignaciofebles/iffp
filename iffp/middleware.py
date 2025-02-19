from django.shortcuts import redirect
from django.urls import reverse_lazy
# from django.urls import reverse
# import logging


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


# class LoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         allowed_urls = [
#             reverse_lazy('loguear'),
#             reverse_lazy('Autenticacion'),
#             reverse_lazy('politica_cookies')
#         ]

#         # Convertir las URLs a cadenas antes de comparar con request.path
#         if not request.user.is_authenticated and request.path not in [str(url) for url in allowed_urls]:
#             return redirect('loguear')

#         return self.get_response(request)


# from django.shortcuts import redirect
# from django.urls import reverse

# class LoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         allowed_paths = [
#             reverse('loguear'),
#             reverse('Autenticacion'),
#             reverse('politica_cookies'),
#         ]

#         print(f'Usuario autenticado: {request.user.is_authenticated}')
#         print(f'Ruta actual: {request.path}')
#         print(f'Rutas permitidas: {allowed_paths}')

#         if not request.user.is_authenticated and not any(request.path.startswith(url) for url in allowed_paths):
#             return redirect('loguear')


#         return self.get_response(request)


# from django.shortcuts import redirect
# from django.urls import reverse

# class LoginRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         allowed_paths = [
#             reverse('loguear'),
#             reverse('Autenticacion'),
#             reverse('politica_cookies'),
#         ]

#         print(f'Usuario autenticado: {request.user.is_authenticated}')
#         print(f'Ruta actual: {request.path}')
#         print(f'Rutas permitidas: {allowed_paths}')

#         # Si el usuario no está autenticado y la ruta no está en allowed_paths
#         if not request.user.is_authenticated:
#             # Si la ruta actual no está en las rutas permitidas
#             if request.path not in allowed_paths:
#                 return redirect('loguear')

#         return self.get_response(request)
