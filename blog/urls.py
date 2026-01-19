from django.urls import path
from . import views

urlpatterns = [

    # ======================
    # PUBLIC
    # ======================
    path('', views.index, name='home'),
    path('kontak/', views.kontak, name='kontak'),
    path('profil/', views.profil, name='profil'),
    path(
        'profil/struktur-organisasi/',
        views.struktur_organisasi,
        name='struktur_organisasi'
    ),

    # ======================
    # BERITA
    # ======================
    path('berita/', views.berita, name='berita'),
    path('berita/<slug:slug>/', views.detail_berita, name='detail_berita'),

    # ======================
    # PRESTASI (PUBLIC)
    # ======================
    path('prestasi/', views.prestasi, name='prestasi'),

    # ======================
    # BIDANG
    # ======================
    path('bidang/<slug:slug>/', views.detail_bidang, name='detail_bidang'),

    # GALERI PUBLIC
    path('galeri/', views.galeri, name='galeri'),

    # ======================
    # AUTH
    # ======================
    path('login/', views.login_public, name='login'),
    path('editor/logout/', views.logout_editor, name='logout'),

    # ======================
    # EDITOR
    # ======================
    path('editor/dashboard/', views.dashboard_editor, name='editor_dashboard'),
    path('editor/moderasi/', views.moderasi_berita, name='moderasi_berita'),
    path('editor/publish/<int:post_id>/', views.publish_berita, name='publish_berita'),
    path('editor/edit/<int:post_id>/', views.edit_berita, name='edit_berita'),
    path('editor/hapus/<int:post_id>/', views.hapus_berita, name='hapus_berita'),  # 🔥 WAJIB
    path('editor/tambah/', views.tambah_berita, name='tambah_berita'),
    path('editor/berita/', views.semua_berita, name='semua_berita'),
    
    # GALERI EDITOR
    path('editor/galeri/', views.editor_galeri, name='editor_galeri'),
    path('editor/galeri/tambah/', views.tambah_galeri, name='tambah_galeri'),
    path('editor/galeri/hapus/<int:id>/', views.hapus_galeri, name='hapus_galeri'),

    # ======================
    # PRESTASI (EDITOR CRUD)
    # ======================
    path('editor/prestasi/', views.editor_prestasi, name='editor_prestasi'),
    path('editor/prestasi/tambah/', views.tambah_prestasi, name='tambah_prestasi'),
    path('editor/prestasi/edit/<int:id>/', views.edit_prestasi, name='edit_prestasi'),
    path('editor/prestasi/hapus/<int:id>/', views.hapus_prestasi, name='hapus_prestasi'),
]

