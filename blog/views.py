import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden
from .models import Galeri, GaleriKategori
from .models import Prestasi

from .models import (
    Post,
    Bidang,
    PersonilBidang,
    ProgramKerja,
    Pengurus,
    Prestasi,
    Galeri,
    GaleriKategori,
)

# =====================================================
# HELPER
# =====================================================
def generate_unique_slug(title):
    base_slug = slugify(title)
    slug = base_slug
    counter = 1
    while Post.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug


# =====================================================
# PUBLIC
# =====================================================
def index(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')[:3]
    return render(request, 'public/home/index.html', {'posts': posts})


def kontak(request):
    return render(request, 'public/Kontak/kontak.html')


def profil(request):
    return render(request, 'public/Profil/tentang.html')


def struktur_organisasi(request):
    return render(
        request,
        'public/Profil/strukturorganisasi.html',
        {
            'pimpinan': Pengurus.objects.all(),
            'bidang_list': Bidang.objects.all(),
        }
    )


def berita(request):
    return render(
        request,
        'public/Seputar_ipmmera/berita_list.html',
        {
            'posts': Post.objects.filter(is_published=True).order_by('-created_at')
        }
    )


def detail_berita(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, 'public/Seputar_ipmmera/berita_detail.html', {'post': post})


# =====================================================
# BIDANG
# =====================================================
def detail_bidang(request, slug):
    bidang = get_object_or_404(Bidang, slug=slug)
    return render(
        request,
        'public/Bidang/detail_bidang.html',
        {
            'bidang': bidang,
            'pimpinan_harian': PersonilBidang.objects.filter(
                bidang=bidang, jabatan__in=['ketua', 'sekretaris']
            ),
            'anggota': PersonilBidang.objects.filter(
                bidang=bidang, jabatan='anggota'
            ),
            'program_kerja': ProgramKerja.objects.filter(bidang=bidang),
        }
    )


# =====================================================
# AUTH
# =====================================================
def login_public(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if user:
            login(request, user)
            return redirect(
                'editor_dashboard'
                if user.groups.filter(name__in=['Admin', 'Editor']).exists()
                else 'home'
            )
        messages.error(request, 'Username atau password salah')

    return render(request, 'public/login.html')


def logout_editor(request):
    logout(request)
    return redirect('login')


# =====================================================
# EDITOR DASHBOARD
# =====================================================
@login_required
def dashboard_editor(request):
    if request.user.groups.filter(name='Kader').exists():
        return redirect('home')

    return render(
        request,
        'editor/dashboard_editor.html',
        {
            'total': Post.objects.count(),
            'draft': Post.objects.filter(is_published=False).count(),
            'publish': Post.objects.filter(is_published=True).count(),
            'draft_terbaru': Post.objects.filter(is_published=False)[:5],
        }
    )


@login_required
def tambah_berita(request):
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    if request.method == 'POST':
        Post.objects.create(
            title=request.POST.get('title'),
            slug=generate_unique_slug(request.POST.get('title')),
            content=request.POST.get('content'),
            thumbnail=request.FILES.get('thumbnail'),
            is_published=False,
        )
        return redirect('editor_dashboard')

    return render(request, 'editor/tambah_berita.html')


@login_required
def moderasi_berita(request):
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    return render(
        request,
        'editor/moderasi_berita.html',
        {
            'posts': Post.objects.filter(is_published=False),
        }
    )


@login_required
def publish_berita(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_published = True
    post.save()
    return redirect('moderasi_berita')


@login_required
def edit_berita(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        if request.FILES.get('thumbnail'):
            post.thumbnail = request.FILES['thumbnail']
        post.save()
        return redirect('moderasi_berita')

    return render(request, 'editor/edit_berita.html', {'post': post})


@login_required
def semua_berita(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden()
    return render(
        request,
        'editor/semua_berita.html',
        {'posts': Post.objects.all()}
    )


@login_required
def hapus_berita(request, post_id):
    if request.method == 'POST' and request.user.groups.filter(name='Admin').exists():
        Post.objects.filter(id=post_id).delete()
    return redirect('semua_berita')


# =====================================================
# PRESTASI
# =====================================================
def prestasi(request):
    qs = Prestasi.objects.select_related('bidang')
    if request.GET.get('tingkat'):
        qs = qs.filter(tingkat=request.GET['tingkat'])
    if request.GET.get('bidang'):
        qs = qs.filter(bidang_id=request.GET['bidang'])

    return render(
        request,
        'public/Seputar_ipmmera/prestasikader.html',
        {
            'prestasi_list': qs,
            'bidang_list': Bidang.objects.all(),
        }
    )


# =====================================================
# GALERI
# =====================================================
def galeri(request):
    qs = Galeri.objects.select_related('kategori')
    if request.GET.get('kategori'):
        qs = qs.filter(kategori_id=request.GET['kategori'])

    return render(
        request,
        'public/Seputar_ipmmera/galeri.html',
        {
            'galeri_list': qs,
            'kategori_list': GaleriKategori.objects.all(),
        }
    )
# ======================
# GALERI (EDITOR)
# ======================
@login_required
def editor_galeri(request):
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    galeri_qs = Galeri.objects.select_related('kategori').order_by('-created_at')
    kategori_list = GaleriKategori.objects.all()

    kategori_id = request.GET.get('kategori')
    if kategori_id:
        galeri_qs = galeri_qs.filter(kategori_id=kategori_id)

    return render(
        request,
        'editor/galeri_list.html',
        {
            'galeri_list': galeri_qs,
            'kategori_list': kategori_list,
            'kategori_aktif': kategori_id,
        }
    )


# ======================
# GALERI (EDITOR)
# ======================
@login_required
def tambah_galeri(request):
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    if request.method == 'POST':
        kategori_id = request.POST.get('kategori')
        judul = request.POST.get('judul')
        files = request.FILES.getlist('foto')

        for f in files:
            Galeri.objects.create(
                kategori_id=kategori_id,
                judul=judul,
                foto=f
            )

        return redirect('editor_galeri')

    return render(
        request,
        'editor/galeri_form.html',
        {
            'kategori_list': GaleriKategori.objects.all()
        }
    )

@login_required
def hapus_galeri(request, id):
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    if request.method == 'POST':
        Galeri.objects.filter(id=id).delete()

    return redirect('editor_galeri')
# ======================
# PRESTASI (EDITOR)
# ======================
@login_required
def editor_prestasi(request):
    # Hanya Admin & Editor
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden("Tidak punya akses")

    prestasi_list = Prestasi.objects.select_related('bidang').order_by('-tahun')

    return render(
        request,
        'editor/prestasi_list.html',
        {
            'prestasi_list': prestasi_list
        }
    )

@login_required
def tambah_prestasi(request):
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    if request.method == 'POST':
        Prestasi.objects.create(
            nama=request.POST.get('nama'),
            capaian=request.POST.get('capaian'),
            bidang_id=request.POST.get('bidang') or None,
            tingkat=request.POST.get('tingkat'),
            tahun=request.POST.get('tahun'),
            keterangan=request.POST.get('keterangan', ''),
            foto=request.FILES.get('foto'),
        )
        return redirect('editor_prestasi')

    return render(
        request,
        'editor/prestasi_form.html',
        {
            'bidang_list': Bidang.objects.all()
        }
    )

@login_required
def edit_prestasi(request, id):
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    prestasi = get_object_or_404(Prestasi, id=id)

    if request.method == 'POST':
        prestasi.nama = request.POST.get('nama')
        prestasi.capaian = request.POST.get('capaian')
        prestasi.bidang_id = request.POST.get('bidang') or None
        prestasi.tingkat = request.POST.get('tingkat')
        prestasi.tahun = request.POST.get('tahun')
        prestasi.keterangan = request.POST.get('keterangan', '')

        if request.FILES.get('foto'):
            prestasi.foto = request.FILES['foto']

        prestasi.save()
        return redirect('editor_prestasi')

    return render(
        request,
        'editor/prestasi_form.html',
        {
            'prestasi': prestasi,
            'bidang_list': Bidang.objects.all(),
        }
    )
@login_required
def hapus_prestasi(request, id):
    # Hanya Admin & Editor yang boleh
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden("Tidak punya akses")

    # Wajib POST (aman, tidak bisa diakses via URL langsung)
    if request.method != 'POST':
        return HttpResponseForbidden("Metode tidak diizinkan")

    prestasi = get_object_or_404(Prestasi, id=id)
    prestasi.delete()

    return redirect('editor_prestasi')
