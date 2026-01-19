from django.shortcuts import redirect
from django.urls import reverse

class EditorRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            if user.groups.filter(name__in=['Admin', 'Editor']).exists():
                # halaman publik yang TIDAK boleh dibuka editor
                forbidden_paths = [
                    reverse('home'),
                    reverse('login'),
                ]

                if request.path in forbidden_paths:
                    return redirect('editor_dashboard')

        return self.get_response(request)
