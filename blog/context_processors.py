def global_user_role(request):
    user = request.user
    return {
        'is_editor': (
            user.is_authenticated and
            user.groups.filter(name__in=['Dewa', 'admin']).exists()
        ),
        'is_dewa': (
            user.is_authenticated and
            user.groups.filter(name='Dewa').exists()
        ),
    }
