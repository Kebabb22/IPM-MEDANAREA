from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Post

@login_required
def dashboard_editor(request):
    if request.user.groups.filter(name='Kader').exists():
        return redirect('home')

    return render(request, 'editor/dashboard_editor.html', {
        'total': Post.objects.count(),
        'draft': Post.objects.filter(is_published=False).count(),
        'publish': Post.objects.filter(is_published=True).count(),
        'is_admin': request.user.groups.filter(name='Admin').exists()
    })


@login_required
def moderasi_berita(request):
    if not request.user.groups.filter(name__in=['Editor', 'Admin']).exists():
        return HttpResponseForbidden("Tidak punya akses")

    return render(request, 'editor/moderasi_berita.html', {
        'posts': Post.objects.filter(is_published=False),
        'is_admin': request.user.groups.filter(name='Admin').exists(),
        'is_editor': request.user.groups.filter(name='Editor').exists(),
    })


@login_required
def publish_berita(request, post_id):
    if not request.user.groups.filter(name__in=['Editor', 'Admin']).exists():
        return HttpResponseForbidden()

    post = get_object_or_404(Post, id=post_id)
    post.is_published = True
    post.save()
    return redirect('moderasi_berita')


@login_required
def hapus_berita(request, post_id):
    if request.method != 'POST':
        return HttpResponseForbidden()

    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden()

    post = get_object_or_404(Post, id=post_id)
    post.delete()
    messages.success(request, "Berita dihapus")
    return redirect('semua_berita')
