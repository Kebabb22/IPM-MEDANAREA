from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import (
    Post,
    Bidang,
    PersonilBidang,
    ProgramKerja,
    Prestasi,
    Galeri,
    GaleriKategori,
    PengelolaWebsite,
    PimpinanUmum,
)

# =====================================================
# HOME
# =====================================================
def index(request):

    posts = Post.objects.filter(
        is_published=True
    ).order_by('-created_at')[:3]

    return render(
        request,
        'public/home/index.html',
        {
            'posts': posts
        }
    )


# =====================================================
# PROFIL
# =====================================================
def profil(request):
    return render(
        request,
        'public/Profil/tentang.html'
    )


# =====================================================
# STRUKTUR ORGANISASI
# =====================================================
def struktur_organisasi(request):

    pimpinan = PimpinanUmum.objects.filter(aktif=True)
    bidang_list = Bidang.objects.all()

    return render(
        request,
        'public/Profil/strukturorganisasi.html',
        {
            'pimpinan': pimpinan,
            'bidang_list': bidang_list,
        }
    )


# =====================================================
# DAFTAR BIDANG
# =====================================================
def bidang(request):

    bidang_list = Bidang.objects.all()

    return render(
        request,
        'public/Bidang/bidang.html',
        {
            'bidang_list': bidang_list
        }
    )


# =====================================================
# DETAIL BIDANG
# =====================================================
def detail_bidang(request, slug):

    bidang = get_object_or_404(
        Bidang,
        slug=slug
    )

    pimpinan_harian = PersonilBidang.objects.filter(
        bidang=bidang,
        jabatan__in=['ketua', 'sekretaris']
    )

    anggota = PersonilBidang.objects.filter(
        bidang=bidang,
        jabatan='anggota'
    )

    program_kerja = ProgramKerja.objects.filter(
        bidang=bidang
    )

    return render(
        request,
        'public/Bidang/detail_bidang.html',
        {
            'bidang': bidang,
            'pimpinan_harian': pimpinan_harian,
            'anggota': anggota,
            'program_kerja': program_kerja,
        }
    )


# =====================================================
# BERITA
# =====================================================
def berita(request):

    qs = Post.objects.filter(
        is_published=True
    ).order_by('-created_at')

    q = request.GET.get('q')

    if q:
        qs = qs.filter(title__icontains=q)

    paginator = Paginator(qs, 6)

    page_obj = paginator.get_page(
        request.GET.get('page')
    )

    return render(
        request,
        'public/Seputar_ipmmera/berita_list.html',
        {
            'page_obj': page_obj,
            'q': q
        }
    )


def detail_berita(request, slug):

    post = get_object_or_404(
        Post,
        slug=slug,
        is_published=True
    )

    return render(
        request,
        'public/Seputar_ipmmera/berita_detail.html',
        {
            'post': post
        }
    )


# =====================================================
# PRESTASI
# =====================================================
def prestasi(request):

    qs = Prestasi.objects.select_related(
        'bidang'
    ).order_by('-tahun')

    paginator = Paginator(qs, 8)

    page_obj = paginator.get_page(
        request.GET.get('page')
    )

    return render(
        request,
        'public/Seputar_ipmmera/prestasikader.html',
        {
            'page_obj': page_obj,
            'bidang_list': Bidang.objects.all(),
        }
    )


# =====================================================
# GALERI
# =====================================================
def galeri(request):

    qs = Galeri.objects.select_related(
        'kategori'
    ).order_by('-created_at')

    paginator = Paginator(qs, 20)

    page_obj = paginator.get_page(
        request.GET.get('page')
    )

    return render(
        request,
        'public/Seputar_ipmmera/galeri.html',
        {
            'page_obj': page_obj,
            'kategori_list': GaleriKategori.objects.all(),
        }
    )

def detail_album(request, judul):

    foto_list = Galeri.objects.filter(judul=judul)

    return render(
        request,
        "public/Seputar_ipmmera/album_detail.html",
        {
            "foto_list": foto_list,
            "judul": judul
        }
    )

# =====================================================
# DONASI
# =====================================================
def donasi(request):
    return render(
        request,
        'public/donasi/donasi.html'
    )


# =====================================================
# KONTAK
# =====================================================
def kontak(request):
    return render(
        request,
        'public/Kontak/Kontak.html'
    )


# =====================================================
# PENGELOLA WEBSITE
# =====================================================
def profil_pengelola(request):

    ketua = PengelolaWebsite.objects.filter(
        role='ketua',
        aktif=True
    ).first()

    editor = PengelolaWebsite.objects.filter(
        role='editor',
        aktif=True
    ).order_by('nama')

    return render(
        request,
        'public/Profil/pengelola.html',
        {
            'ketua': ketua,
            'editor': editor,
            'has_ketua': bool(ketua)
        }
    )