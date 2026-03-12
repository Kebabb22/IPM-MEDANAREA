import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Count, Min

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


# =====================================================
# BERITA (EDITORIAL FLOW)
# =====================================================
@login_required
def tambah_berita(request):
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    if request.method == 'POST':
        title = request.POST.get('title')

        Post.objects.create(
            title=title,
            slug=generate_unique_slug(title),  # FIX: pastikan unik
            content=request.POST.get('content'),
            thumbnail=request.FILES.get('thumbnail'),
            is_published=False,               # FIX: selalu draft
        )

        messages.success(
            request,
            'Berita berhasil disimpan dan menunggu moderasi'
        )  # FIX: feedback UX

        return redirect('semua_berita')

    return render(request, 'editor/tambah_berita.html')

@login_required
def publish_berita(request, post_id):
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    post = get_object_or_404(Post, id=post_id)
    post.is_published = True
    post.save()

    messages.success(request, 'Berita berhasil dipublikasikan')  # FIX
    return redirect('semua_berita')


@login_required
def edit_berita(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.slug = generate_unique_slug(request.POST.get('title'))  # FIX
        post.content = request.POST.get('content')

        if request.FILES.get('thumbnail'):
            post.thumbnail = request.FILES['thumbnail']

        post.save()
        messages.success(request, 'Berita berhasil diperbarui')  # FIX
        return redirect('semua_berita')

    return render(request, 'editor/edit_berita.html', {'post': post})


@login_required
def semua_berita(request):
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden()

    return render(
        request,
        'editor/semua_berita.html',
        {'posts': Post.objects.all().order_by('-created_at')}
    )


@login_required
def hapus_berita(request, post_id):
    if request.method == 'POST' and request.user.groups.filter(name='Admin').exists():
        Post.objects.filter(id=post_id).delete()
        messages.success(request, 'Berita berhasil dihapus')  # FIX

    return redirect('semua_berita')


# =====================================================
# PRESTASI (PUBLIC)
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
# GALERI (PUBLIC)
# =====================================================
def galeri(request):

    album_list = (
        Galeri.objects
        .values('judul')
        .annotate(
            total=Count('id'),
            cover=Min('foto')
        )
        .order_by('-judul')
    )

    return render(
        request,
        "public/Seputar_ipmmera/galeri.html",
        {
            "album_list": album_list
        }
    )

def detail_album(request, judul):

    foto_list = Galeri.objects.filter(judul=judul)

    return render(
        request,
        "public/Seputar_ipmmera/detail_album.html",
        {
            "foto_list": foto_list,
            "judul": judul
        }
    )

# =====================================================
# GALERI (EDITOR)
# =====================================================
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

        messages.success(request, 'Galeri berhasil ditambahkan')  # FIX
        return redirect('editor_galeri')

    return render(
        request,
        'editor/galeri_form.html',
        {'kategori_list': GaleriKategori.objects.all()}
    )


@login_required
def hapus_galeri(request, id):
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    if request.method == 'POST':
        Galeri.objects.filter(id=id).delete()
        messages.success(request, 'Galeri berhasil dihapus')  # FIX

    return redirect('editor_galeri')


# =====================================================
# PRESTASI (EDITOR)
# =====================================================
@login_required
def editor_prestasi(request):
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    prestasi_list = Prestasi.objects.select_related('bidang').order_by('-tahun')

    return render(
        request,
        'editor/prestasi_list.html',
        {'prestasi_list': prestasi_list}
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

        messages.success(request, 'Prestasi berhasil ditambahkan')  # FIX
        return redirect('editor_prestasi')

    return render(
        request,
        'editor/prestasi_form.html',
        {'bidang_list': Bidang.objects.all()}
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
        messages.success(request, 'Prestasi berhasil diperbarui')  # FIX
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
    if not request.user.groups.filter(name__in=['Admin', 'Editor']).exists():
        return HttpResponseForbidden()

    if request.method != 'POST':
        return HttpResponseForbidden()

    Prestasi.objects.filter(id=id).delete()
    messages.success(request, 'Prestasi berhasil dihapus')  # FIX

    return redirect('editor_prestasi')
