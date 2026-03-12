from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.text import slugify
import os

from .models import (
    Post,
    Bidang,
    Prestasi,
    Galeri,
    GaleriKategori,
    PengelolaWebsite,
    PimpinanUmum,
    PersonilBidang,
    ProgramKerja,
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


def editor_only(user):
    """
    Akses editor:
    - Dewa (full access)
    - admin (editor role)
    """
    return (
        user.is_authenticated and
        user.groups.filter(name__in=['Dewa', 'admin']).exists()
    )


def admin_only(user):
    """
    Akses admin penuh (opsional)
    """
    return (
        user.is_authenticated and
        user.groups.filter(name='Dewa').exists()
    )


# =====================================================
# DASHBOARD
# =====================================================
# =====================================================
# BERITA (EDITOR)
# =====================================================

@login_required
def dashboard_editor(request):

    if not editor_only(request.user):
        return HttpResponseForbidden("Akun Anda tidak memiliki akses ke halaman ini.")

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

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    if request.method == 'POST':

        title = request.POST.get('title')

        Post.objects.create(
            title=title,
            slug=generate_unique_slug(title),
            content=request.POST.get('content'),
            thumbnail=request.FILES.get('thumbnail'),
            is_published=False,
        )

        messages.success(
            request,
            'Berita berhasil disimpan'
        )

        return redirect('semua_berita')

    return render(
        request,
        'editor/berita/tambah_berita.html'
    )





@login_required
def publish_berita(request, post_id):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    post = get_object_or_404(Post, id=post_id)
    post.is_published = True
    post.save()

    messages.success(request, 'Berita berhasil dipublikasikan')
    return redirect('semua_berita')


@login_required
def edit_berita(request, post_id):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        title = request.POST.get('title')

        post.title = title
        post.slug = generate_unique_slug(title)
        post.content = request.POST.get('content')

        if request.FILES.get('thumbnail'):
            post.thumbnail = request.FILES['thumbnail']

        post.save()
        messages.success(request, 'Berita berhasil diperbarui')
        return redirect('semua_berita')

    return render(
        request,
        'editor/berita/edit_berita.html',
        {'post': post}
    )


@login_required
def semua_berita(request):
    if not admin_only(request.user):
        return HttpResponseForbidden("Hanya Dewa")

    return render(
        request,
        'editor/berita/semua_berita.html',
        {'posts': Post.objects.all().order_by('-created_at')}
    )


@login_required
def hapus_berita(request, post_id):
    if not admin_only(request.user):
        return HttpResponseForbidden("Hanya Dewa")

    if request.method == 'POST':
        Post.objects.filter(id=post_id).delete()
        messages.success(request, 'Berita berhasil dihapus')

    return redirect('semua_berita')


# =====================================================
# PRESTASI (EDITOR)
# =====================================================
@login_required
def editor_prestasi(request):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    prestasi_list = Prestasi.objects.select_related('bidang').order_by('-tahun')

    return render(
        request,
        'editor/prestasi/prestasi_list.html',
        {'prestasi_list': prestasi_list}
    )


@login_required
def tambah_prestasi(request):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

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

        messages.success(request, 'Prestasi berhasil ditambahkan')
        return redirect('editor_prestasi')

    return render(
        request,
        'editor/prestasi/prestasi_form.html',
        {'bidang_list': Bidang.objects.all()}
    )


@login_required
def edit_prestasi(request, id):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

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
        messages.success(request, 'Prestasi berhasil diperbarui')
        return redirect('editor_prestasi')

    return render(
        request,
        'editor/prestasi/prestasi_form.html',
        {
            'prestasi': prestasi,
            'bidang_list': Bidang.objects.all(),
        }
    )


@login_required
def hapus_prestasi(request, id):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    if request.method == 'POST':
        Prestasi.objects.filter(id=id).delete()
        messages.success(request, 'Prestasi berhasil dihapus')

    return redirect('editor_prestasi')


# =====================================================
# GALERI (EDITOR)
# =====================================================
@login_required
def editor_galeri(request):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    galeri_qs = Galeri.objects.select_related('kategori').order_by('-created_at')
    kategori_list = GaleriKategori.objects.all()

    kategori_id = request.GET.get('kategori')
    if kategori_id:
        galeri_qs = galeri_qs.filter(kategori_id=kategori_id)

    return render(
        request,
        'editor/galeri/galeri_list.html',
        {
            'galeri_list': galeri_qs,
            'kategori_list': kategori_list,
            'kategori_aktif': kategori_id,
        }
    )


def tambah_galeri(request):

    if request.method == "POST":

        judul = request.POST.get("judul")
        files = request.FILES.getlist("foto")

        objs = []

        for f in files:
            objs.append(
                Galeri(
                    judul=judul,
                    foto=f
                )
            )

        Galeri.objects.bulk_create(objs)

        messages.success(request, "Foto berhasil diupload")

        return redirect("editor_galeri")

    return render(
        request,
        "editor/galeri/galeri_form.html"
    )

@login_required
def hapus_galeri(request, id):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    if request.method == 'POST':
        Galeri.objects.filter(id=id).delete()
        messages.success(request, 'Galeri berhasil dihapus')

    return redirect('editor_galeri')

# =====================================================
# PIMPINAN UMUM (EDITOR)
# =====================================================

@login_required
def pimpinan_list(request):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    pimpinan = PimpinanUmum.objects.all()

    return render(
        request,
        'editor/pimpinan_umum/list.html',
        {'pimpinan': pimpinan}
    )


@login_required
def pimpinan_tambah(request):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    if request.method == "POST":

        PimpinanUmum.objects.create(
            nama=request.POST.get("nama"),
            jabatan=request.POST.get("jabatan"),
            foto=request.FILES.get("foto")
        )

        messages.success(request, "Pimpinan berhasil ditambahkan")
        return redirect("editor_pimpinan")

    return render(request, 'editor/pimpinan_umum/tambah.html')


@login_required
def pimpinan_edit(request, id):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    pimpinan = get_object_or_404(PimpinanUmum, id=id)

    if request.method == "POST":

        pimpinan.nama = request.POST.get("nama")
        pimpinan.jabatan = request.POST.get("jabatan")

        if request.FILES.get("foto"):
            pimpinan.foto = request.FILES.get("foto")

        pimpinan.save()

        messages.success(request, "Pimpinan berhasil diperbarui")
        return redirect("editor_pimpinan")

    return render(
        request,
        'editor/pimpinan_umum/tambah.html',
        {'pimpinan': pimpinan}
    )


@login_required
def pimpinan_hapus(request, id):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    pimpinan = get_object_or_404(PimpinanUmum, id=id)
    pimpinan.delete()

    messages.success(request, "Pimpinan berhasil dihapus")

    return redirect('editor_pimpinan')

# DETAIL BIDANG EDITOR


# =====================================================
# BIDANG (EDITOR)
# =====================================================

@login_required
def editor_bidang(request):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    bidang_list = Bidang.objects.all()

    return render(
        request,
        'editor/bidang/list.html',
        {
            'bidang_list': bidang_list
        }
    )


@login_required
def tambah_bidang(request):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    if request.method == "POST":

        Bidang.objects.create(
            nama=request.POST.get("nama"),
            slug=request.POST.get("slug"),
            deskripsi=request.POST.get("deskripsi"),
            foto=request.FILES.get("foto")
        )

        messages.success(request, "Bidang berhasil ditambahkan")

        return redirect("editor_bidang")

    return render(request, "editor/bidang/form.html")


@login_required
def edit_bidang(request, id):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    bidang = get_object_or_404(Bidang, id=id)

    if request.method == "POST":

        bidang.nama = request.POST.get("nama")
        bidang.slug = request.POST.get("slug")
        bidang.deskripsi = request.POST.get("deskripsi")

        if request.FILES.get("foto"):
            bidang.foto = request.FILES.get("foto")

        bidang.save()

        messages.success(request, "Bidang berhasil diperbarui")

        return redirect("editor_bidang")

    return render(
        request,
        "editor/bidang/form.html",
        {"bidang": bidang}
    )


@login_required
def hapus_bidang(request, id):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    bidang = get_object_or_404(Bidang, id=id)

    bidang.delete()

    messages.success(request, "Bidang berhasil dihapus")

    return redirect("editor_bidang")

#EDITOR PERSONIL BIDANG
# =====================================================
# PERSONIL BIDANG (EDITOR)
# =====================================================

@login_required
def editor_personil_bidang(request):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    data = PersonilBidang.objects.select_related('bidang').order_by('urutan')

    return render(
        request,
        'editor/personil_bidang/list.html',
        {'data': data}
    )


@login_required
def tambah_personil_bidang(request):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    if request.method == "POST":

        PersonilBidang.objects.create(
            bidang_id=request.POST.get("bidang"),
            nama=request.POST.get("nama"),
            jabatan=request.POST.get("jabatan"),
            urutan=request.POST.get("urutan", 0),
            foto=request.FILES.get("foto")
        )

        messages.success(request, "Personil bidang berhasil ditambahkan")

        return redirect("editor_personil_bidang")

    return render(
        request,
        'editor/personil_bidang/form.html',
        {
            'bidang_list': Bidang.objects.all()
        }
    )


@login_required
def edit_personil_bidang(request, id):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    obj = get_object_or_404(PersonilBidang, id=id)

    if request.method == "POST":

        obj.bidang_id = request.POST.get("bidang")
        obj.nama = request.POST.get("nama")
        obj.jabatan = request.POST.get("jabatan")
        obj.urutan = request.POST.get("urutan", 0)

        if request.FILES.get("foto"):
            obj.foto = request.FILES.get("foto")

        obj.save()

        messages.success(request, "Personil bidang berhasil diperbarui")

        return redirect("editor_personil_bidang")

    return render(
        request,
        'editor/personil_bidang/form.html',
        {
            'obj': obj,
            'bidang_list': Bidang.objects.all()
        }
    )


@login_required
def hapus_personil_bidang(request, id):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    obj = get_object_or_404(PersonilBidang, id=id)
    obj.delete()

    messages.success(request, "Personil bidang berhasil dihapus")

    return redirect("editor_personil_bidang")

# =====================================================
# PROGRAM KERJA (EDITOR)
# =====================================================

@login_required
def editor_program_kerja(request):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    data = ProgramKerja.objects.select_related('bidang').order_by('-tanggal')

    return render(
        request,
        'editor/program_kerja/list.html',
        {'data': data}
    )


@login_required
def tambah_program_kerja(request):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    if request.method == "POST":

        ProgramKerja.objects.create(
            bidang_id=request.POST.get("bidang"),
            judul=request.POST.get("judul"),
            deskripsi=request.POST.get("deskripsi"),
            tanggal=request.POST.get("tanggal"),
            foto=request.FILES.get("foto")
        )

        messages.success(request, "Program kerja berhasil ditambahkan")

        return redirect("editor_program_kerja")

    return render(
        request,
        'editor/program_kerja/form.html',
        {
            'bidang_list': Bidang.objects.all()
        }
    )


@login_required
def edit_program_kerja(request, id):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    obj = get_object_or_404(ProgramKerja, id=id)

    if request.method == "POST":

        obj.bidang_id = request.POST.get("bidang")
        obj.judul = request.POST.get("judul")
        obj.deskripsi = request.POST.get("deskripsi")
        obj.tanggal = request.POST.get("tanggal")

        if request.FILES.get("foto"):
            obj.foto = request.FILES.get("foto")

        obj.save()

        messages.success(request, "Program kerja berhasil diperbarui")

        return redirect("editor_program_kerja")

    return render(
        request,
        'editor/program_kerja/form.html',
        {
            'obj': obj,
            'bidang_list': Bidang.objects.all()
        }
    )


@login_required
def hapus_program_kerja(request, id):

    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    obj = get_object_or_404(ProgramKerja, id=id)
    obj.delete()

    messages.success(request, "Program kerja berhasil dihapus")

    return redirect("editor_program_kerja")

# =====================================================
# PENGELOLA WEBSITE (EDITOR)
# =====================================================
@login_required
def pengelola_list(request):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    data = PengelolaWebsite.objects.all().order_by('role', 'id')
    return render(
        request,
        'editor/pengelola/pengelola_list.html',
        {'data': data}
    )


@login_required
def pengelola_tambah(request):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    if request.method == 'POST':
        foto = request.FILES.get('foto')

        if foto:
            if foto.content_type not in ['image/jpeg', 'image/png', 'image/webp']:
                messages.error(request, 'Format foto harus JPG, PNG, atau WEBP')
                return redirect('editor_pengelola_tambah')

            if foto.size > 2 * 1024 * 1024:
                messages.error(request, 'Ukuran foto maksimal 2MB')
                return redirect('editor_pengelola_tambah')

        PengelolaWebsite.objects.create(
            nama=request.POST.get('nama'),
            organisasi=request.POST.get('organisasi'),
            role=request.POST.get('role'),
            foto=foto,
            aktif=True
        )

        messages.success(request, 'Pengelola berhasil ditambahkan')
        return redirect('editor_pengelola')


@login_required
def pengelola_edit(request, id):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    obj = get_object_or_404(PengelolaWebsite, id=id)

    if request.method == 'POST':
        foto = request.FILES.get('foto')

        if foto:
            if foto.content_type not in ['image/jpeg', 'image/png', 'image/webp']:
                messages.error(request, 'Format foto harus JPG, PNG, atau WEBP')
                return redirect('editor_pengelola_edit', id=id)

            if foto.size > 2 * 1024 * 1024:
                messages.error(request, 'Ukuran foto maksimal 2MB')
                return redirect('editor_pengelola_edit', id=id)

            if obj.foto and os.path.isfile(obj.foto.path):
                os.remove(obj.foto.path)

            obj.foto = foto

        obj.nama = request.POST.get('nama')
        obj.organisasi = request.POST.get('organisasi')
        obj.role = request.POST.get('role')
        obj.save()

        messages.success(request, 'Pengelola berhasil diperbarui')
        return redirect('editor_pengelola')


@login_required
def pengelola_hapus(request, id):
    if not editor_only(request.user):
        return HttpResponseForbidden("Tidak punya akses")

    obj = get_object_or_404(PengelolaWebsite, id=id)

    if obj.foto and os.path.isfile(obj.foto.path):
        os.remove(obj.foto.path)

    obj.delete()
    messages.success(request, 'Pengelola berhasil dihapus')

    return redirect('editor_pengelola')
