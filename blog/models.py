from django.db import models
from PIL import Image


# =====================================================
# POST / BERITA
# =====================================================
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='berita/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.thumbnail:
            try:
                img = Image.open(self.thumbnail.path)
                max_size = (800, 800)
                if img.height > 800 or img.width > 800:
                    img.thumbnail(max_size)
                    img.save(self.thumbnail.path)
            except Exception:
                pass


# =====================================================
# BIDANG
# =====================================================
class Bidang(models.Model):
    nama = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    deskripsi = models.TextField(blank=True)

    def __str__(self):
        return self.nama


# =====================================================
# PERSONIL BIDANG
# =====================================================
class PersonilBidang(models.Model):
    JABATAN_CHOICES = [
        ('ketua', 'Ketua Bidang'),
        ('sekretaris', 'Sekretaris Bidang'),
        ('anggota', 'Anggota'),
    ]

    bidang = models.ForeignKey(Bidang, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=20, choices=JABATAN_CHOICES)
    foto = models.ImageField(upload_to='personil/', blank=True, null=True)
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['urutan']

    def __str__(self):
        return f"{self.nama} - {self.get_jabatan_display()}"


# =====================================================
# PROGRAM KERJA
# =====================================================
class ProgramKerja(models.Model):
    bidang = models.ForeignKey(Bidang, on_delete=models.CASCADE)
    judul = models.CharField(max_length=150)
    deskripsi = models.TextField()
    foto = models.ImageField(upload_to='program/')
    tanggal = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.judul


# =====================================================
# PENGURUS
# =====================================================
class Pengurus(models.Model):
    nama = models.CharField(max_length=100)
    jabatan = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='pengurus/', blank=True, null=True)
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['urutan']

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"


# =====================================================
# PRESTASI
# =====================================================
class Prestasi(models.Model):
    nama = models.CharField(max_length=150)
    bidang = models.ForeignKey(
        Bidang,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    capaian = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='prestasi/', blank=True, null=True)
    tingkat = models.CharField(
        max_length=30,
        choices=[
            ('lokal', 'Lokal'),
            ('daerah', 'Daerah'),
            ('nasional', 'Nasional'),
            ('internasional', 'Internasional'),
        ]
    )
    tahun = models.PositiveIntegerField()
    keterangan = models.TextField(blank=True)

    class Meta:
        ordering = ['-tahun']

    def __str__(self):
        return f"{self.nama} - {self.capaian}"


# =====================================================
# GALERI
# =====================================================
class GaleriKategori(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


class Galeri(models.Model):
    kategori = models.ForeignKey(
        GaleriKategori,
        on_delete=models.CASCADE,
        related_name='galeri',
        null=True,        # ✅ PENTING (biar data lama aman)
        blank=True        # ✅ biar form admin/editor fleksibel
    )
    judul = models.CharField(max_length=150)
    foto = models.ImageField(upload_to='galeri/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul
