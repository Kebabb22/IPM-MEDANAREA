from django.contrib import admin
from .models import (
    Post,
    Bidang,
    PersonilBidang,
    ProgramKerja,
    Pengurus,
    Prestasi,
    Galeri,
    GaleriKategori
)

# =====================================================
# POST / BERITA
# =====================================================
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_at",)


# =====================================================
# BIDANG
# =====================================================
@admin.register(Bidang)
class BidangAdmin(admin.ModelAdmin):
    list_display = ("nama",)
    prepopulated_fields = {"slug": ("nama",)}
    search_fields = ("nama",)


# =====================================================
# PERSONIL BIDANG
# =====================================================
@admin.register(PersonilBidang)
class PersonilBidangAdmin(admin.ModelAdmin):
    list_display = ("nama", "bidang", "jabatan", "urutan")
    list_filter = ("bidang", "jabatan")
    search_fields = ("nama",)
    ordering = ("bidang", "urutan")


# =====================================================
# PROGRAM KERJA
# =====================================================
@admin.register(ProgramKerja)
class ProgramKerjaAdmin(admin.ModelAdmin):
    list_display = ("judul", "bidang", "tanggal")
    list_filter = ("bidang",)
    search_fields = ("judul",)


# =====================================================
# PENGURUS
# =====================================================
@admin.register(Pengurus)
class PengurusAdmin(admin.ModelAdmin):
    list_display = ("nama", "jabatan", "urutan")
    ordering = ("urutan",)
    search_fields = ("nama", "jabatan")


# =====================================================
# PRESTASI
# =====================================================
@admin.register(Prestasi)
class PrestasiAdmin(admin.ModelAdmin):
    list_display = ("nama", "bidang", "capaian", "tingkat", "tahun")
    list_filter = ("tingkat", "tahun", "bidang")
    search_fields = ("nama", "capaian")


# =====================================================
# GALERI
# =====================================================
@admin.register(GaleriKategori)
class GaleriKategoriAdmin(admin.ModelAdmin):
    search_fields = ("nama",)



@admin.register(Galeri)
class GaleriAdmin(admin.ModelAdmin):
    list_display = ("judul", "kategori", "created_at")
    list_filter = ("kategori",)
    search_fields = ("judul",)
