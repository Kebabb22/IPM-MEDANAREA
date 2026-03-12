from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# ======================
# LOGIN PUBLIC
# ======================
def login_public(request):
    """
    Login untuk user editor / admin (Dewa & admin).
    User selain itu diarahkan ke home.
    """

    # Kalau sudah login, jangan balik ke login
    if request.user.is_authenticated:
        if request.user.groups.filter(name__in=['Dewa', 'admin']).exists():
            return redirect('editor_dashboard')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_active:
            login(request, user)

            # 🔐 Role-based redirect
            if user.groups.filter(name__in=['Dewa', 'admin']).exists():
                return redirect('editor_dashboard')

            # User biasa
            messages.warning(
                request,
                'Akun Anda tidak memiliki akses editor'
            )
            return redirect('home')

        # Login gagal
        messages.error(
            request,
            'Username atau password salah'
        )

    return render(request, 'public/login.html')


# ======================
# LOGOUT EDITOR
# ======================
def logout_editor(request):
    """
    Logout user editor / admin.
    """
    logout(request)
    return redirect('home')
