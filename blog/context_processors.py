def global_user_role(request):
    is_editor = False

    if request.user.is_authenticated:
        is_editor = request.user.groups.filter(
            name__in=['Admin', 'Editor']
        ).exists()

    return {
        'is_editor': is_editor
    }
