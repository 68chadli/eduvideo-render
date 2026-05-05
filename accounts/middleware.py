from .models import LogConnexion

class LogConnexionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated and request.method == 'POST' and request.path == '/accounts/login/':
            ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
            if ip:
                ip = ip.split(',')[0].strip()
            LogConnexion.objects.create(utilisateur=request.user, ip_adresse=ip)
        
        return response