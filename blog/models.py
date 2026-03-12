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

    foto = models.ImageField(
        upload_to='bidang/',
        blank=True,
        null=True
    )

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

    bidang = models.ForeignKey(
        Bidang,
        on_delete=models.CASCADE,
        related_name='personil'
    )

    nama = models.CharField(max_length=100)

    jabatan = models.CharField(
        max_length=20,
        choices=JABATAN_CHOICES
    )

    foto = models.ImageField(
        upload_to='personil_bidang/',
        blank=True,
        null=True
    )

    urutan = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nama} - {self.bidang.nama}"


# =====================================================
# PROGRAM KERJA
# =====================================================
class ProgramKerja(models.Model):

    bidang = models.ForeignKey(
        Bidang,
        on_delete=models.CASCADE,
        related_name='program'
    )

    judul = models.CharField(max_length=200)

    deskripsi = models.TextField()

    foto = models.ImageField(
        upload_to='program_kerja/',
        blank=True,
        null=True
    )

    tanggal = models.DateField(blank=True, null=True)

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
        null=True,
        blank=True
    )

    judul = models.CharField(max_length=150)
    foto = models.ImageField(upload_to='galeri/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.judul

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        try:
            img = Image.open(self.foto.path)

            max_size = (1600, 1600)
            if img.height > 1600 or img.width > 1600:
                img.thumbnail(max_size)

            img.save(self.foto.path, optimize=True, quality=75)
        except Exception:
            pass

#data pimpinan umum #
class PimpinanUmum(models.Model):
    nama = models.CharField(max_length=150)
    jabatan = models.CharField(max_length=150)
    foto = models.ImageField(upload_to='pimpinan/', blank=True, null=True)

    aktif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nama} - {self.jabatan}"
    
# pengelolas website #

class PengelolaWebsite(models.Model):
    ROLE_CHOICES = [
        ('ketua', 'Ketua'),
        ('editor', 'Editor'),
    ]

    nama = models.CharField(max_length=150)
    organisasi = models.CharField(max_length=150)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    foto = models.ImageField(
        upload_to='pengelola/',
        blank=True,
        null=True
    )

    aktif = models.BooleanField(default=True)

    def __str__(self):
        return self.nama

    @property
    def avatar(self):
        """Avatar default jika belum ada foto"""
        if self.foto:
            return self.foto.url
        return None