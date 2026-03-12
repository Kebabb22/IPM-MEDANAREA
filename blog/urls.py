from django.urls import path

# ======================
# IMPORT VIEWS (MODULAR)
# ======================
from . import views_public
from . import views_editor
from . import views_auth
from . import views

urlpatterns = [

    # ======================
    # PUBLIC / HOME
    # ======================
    path('', views_public.index, name='home'),

    # ======================
    # PROFIL (PUBLIC)
    # ======================
    path('profil/', views_public.profil, name='profil'),
    path(
        'profil/struktur-organisasi/',
        views_public.struktur_organisasi,
        name='struktur_organisasi'
    ),
    path(
        'profil/pengelola/',
        views_public.profil_pengelola,
        name='profil_pengelola'
    ),

    # ======================
    # DONASI
    # ======================
    path('donasi/', views_public.donasi, name='donasi'),

    # ======================
    # KONTAK
    # ======================
    path('kontak/', views_public.kontak, name='kontak'),

    # ======================
    # BERITA (PUBLIC)
    # ======================
    path('berita/', views_public.berita, name='berita'),
    path(
        'berita/<slug:slug>/',
        views_public.detail_berita,
        name='detail_berita'
    ),

    # ======================
    # PRESTASI (PUBLIC)
    # ======================
    path('prestasi/', views_public.prestasi, name='prestasi'),

    # ======================
    # GALERI (PUBLIC)
    # ======================

    path("galeri/", views.galeri, name="galeri"),
    path("galeri/<str:judul>/", views.detail_album, name="detail_album"),

    # ======================
    # BIDANG PUBLIC
    # ======================
    path(
        'bidang/<slug:slug>/',
        views_public.detail_bidang,
        name='detail_bidang'
    ),
    path(
    'bidang/',
    views_public.bidang,
    name='bidang'
    ),

    # ======================
    # AUTH
    # ======================
    path('login/', views_auth.login_public, name='login'),
    path('editor/logout/', views_auth.logout_editor, name='logout'),

    # ======================
    # EDITOR - DASHBOARD
    # ======================
    path(
        'editor/dashboard/',
        views_editor.dashboard_editor,
        name='editor_dashboard'
    ),

    # ======================
    # EDITOR - BERITA
    # ======================
    path(
        'editor/berita/',
        views_editor.semua_berita,
        name='semua_berita'
    ),
    path(
        'editor/berita/tambah/',
        views_editor.tambah_berita,
        name='tambah_berita'
    ),
    path(
        'editor/berita/edit/<int:post_id>/',
        views_editor.edit_berita,
        name='edit_berita'
    ),
    path(
        'editor/berita/hapus/<int:post_id>/',
        views_editor.hapus_berita,
        name='hapus_berita'
    ),
    path(
        'editor/berita/publish/<int:post_id>/',
        views_editor.publish_berita,
        name='publish_berita'
    ),


    # ======================
    # EDITOR - GALERI
    # ======================
    path(
        'editor/galeri/',
        views_editor.editor_galeri,
        name='editor_galeri'
    ),
    path(
        'editor/galeri/tambah/',
        views_editor.tambah_galeri,
        name='tambah_galeri'
    ),
    path(
        'editor/galeri/hapus/<int:id>/',
        views_editor.hapus_galeri,
        name='hapus_galeri'
    ),

    # ======================
    # EDITOR - PRESTASI
    # ======================
    path(
        'editor/prestasi/',
        views_editor.editor_prestasi,
        name='editor_prestasi'
    ),
    path(
        'editor/prestasi/tambah/',
        views_editor.tambah_prestasi,
        name='tambah_prestasi'
    ),
    path(
        'editor/prestasi/edit/<int:id>/',
        views_editor.edit_prestasi,
        name='edit_prestasi'
    ),
    path(
        'editor/prestasi/hapus/<int:id>/',
        views_editor.hapus_prestasi,
        name='hapus_prestasi'
    ),

    # ======================
# EDITOR - PIMPINAN UMUM
# ======================

path(
    'editor/pimpinan_umum/',
    views_editor.pimpinan_list,
    name='editor_pimpinan'
),

path(
    'editor/pimpinan_umum/tambah/',
    views_editor.pimpinan_tambah,
    name='editor_pimpinan_tambah'
),

path(
    'editor/pimpinan_umum/edit/<int:id>/',
    views_editor.pimpinan_edit,
    name='editor_pimpinan_edit'
),

path(
    'editor/pimpinan_umum/hapus/<int:id>/',
    views_editor.pimpinan_hapus,
    name='editor_pimpinan_hapus'
),

    # ======================
# EDITOR - BIDANG
# ======================

path(
    'editor/bidang/',
    views_editor.editor_bidang,
    name='editor_bidang'
),

path(
    'editor/bidang/tambah/',
    views_editor.tambah_bidang,
    name='tambah_bidang'
),

path(
    'editor/bidang/edit/<int:id>/',
    views_editor.edit_bidang,
    name='edit_bidang'
),

path(
    'editor/bidang/hapus/<int:id>/',
    views_editor.hapus_bidang,
    name='hapus_bidang'
),

# PERSONIL BIDANG

path(
    'editor/personil/',
    views_editor.editor_personil_bidang,
    name='editor_personil_bidang'
),

path(
    'editor/personil/tambah/',
    views_editor.tambah_personil_bidang,
    name='tambah_personil_bidang'
),

path(
    'editor/personil/edit/<int:id>/',
    views_editor.edit_personil_bidang,
    name='edit_personil_bidang'
),

path(
    'editor/personil/hapus/<int:id>/',
    views_editor.hapus_personil_bidang,
    name='hapus_personil_bidang'
),


# PROGRAM KERJA

path(
    'editor/program/',
    views_editor.editor_program_kerja,
    name='editor_program_kerja'
),

path(
    'editor/program/tambah/',
    views_editor.tambah_program_kerja,
    name='tambah_program_kerja'
),

path(
    'editor/program/edit/<int:id>/',
    views_editor.edit_program_kerja,
    name='edit_program_kerja'
),

path(
    'editor/program/hapus/<int:id>/',
    views_editor.hapus_program_kerja,
    name='hapus_program_kerja'
),

# PERSONIL BIDANG
path('editor/personil/', views_editor.editor_personil_bidang, name='editor_personil_bidang'),
path('editor/personil/tambah/', views_editor.tambah_personil_bidang, name='tambah_personil_bidang'),
path('editor/personil/edit/<int:id>/', views_editor.edit_personil_bidang, name='edit_personil_bidang'),
path('editor/personil/hapus/<int:id>/', views_editor.hapus_personil_bidang, name='hapus_personil_bidang'),

# PROGRAM KERJA
path('editor/program/', views_editor.editor_program_kerja, name='editor_program_kerja'),
path('editor/program/tambah/', views_editor.tambah_program_kerja, name='tambah_program_kerja'),
path('editor/program/edit/<int:id>/', views_editor.edit_program_kerja, name='edit_program_kerja'),
path('editor/program/hapus/<int:id>/', views_editor.hapus_program_kerja, name='hapus_program_kerja'),

    # ======================
    # EDITOR - PENGELOLA WEBSITE  ✅ (BARU)
    # ======================
    path(
        'editor/pengelola/',
        views_editor.pengelola_list,
        name='editor_pengelola'
    ),
    path(
        'editor/pengelola/tambah/',
        views_editor.pengelola_tambah,
        name='editor_pengelola_tambah'
    ),
    path(
        'editor/pengelola/edit/<int:id>/',
        views_editor.pengelola_edit,
        name='editor_pengelola_edit'
    ),
    path(
        'editor/pengelola/hapus/<int:id>/',
        views_editor.pengelola_hapus,
        name='editor_pengelola_hapus'
    ),
]
