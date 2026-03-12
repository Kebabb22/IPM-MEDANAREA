from django.shortcuts import redirect
from django.urls import reverse


class EditorRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        login_url = reverse('login')

        # Izinkan halaman login & static
        if request.path.startswith(login_url):
            return self.get_response(request)

        if request.user.is_authenticated:
            if request.path.startswith('/editor/'):
                if not request.user.groups.filter(
                    name__in=['Dewa', 'admin']
                ).exists():
                    return redirect('home')

        return self.get_response(request)
