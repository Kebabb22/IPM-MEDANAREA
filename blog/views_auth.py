from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_editor(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:
            login(request, user)

            if user.groups.filter(name='Kader').exists():
                return redirect('home')
            return redirect('editor_dashboard')

        messages.error(request, 'Username atau password salah')

    return render(request, 'editor/login_editor.html')


def logout_editor(request):
    logout(request)
    return redirect('login_editor')
