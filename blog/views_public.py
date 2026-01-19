from django.shortcuts import render, get_object_or_404
from .models import Post, Bidang, PersonilBidang, ProgramKerja

def index(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    return render(request, 'public/home/index.html', {'posts': posts})

def berita(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'public/Seputar_ipmmera/berita_list.html', {'posts': posts})

def detail_berita(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, 'public/Seputar_ipmmera/berita_detail.html', {'post': post})

def detail_bidang(request, slug):
    bidang = get_object_or_404(Bidang, slug=slug)
    personil = PersonilBidang.objects.filter(bidang=bidang).order_by('urutan')
    program = ProgramKerja.objects.filter(bidang=bidang)

    return render(request, 'public/Bidang/detail_bidang.html', {
        'bidang': bidang,
        'personil': personil,
        'program': program,
    })
