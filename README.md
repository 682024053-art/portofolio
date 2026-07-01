# Website Portfolio Flask + TiDB + Cloudinary + Resend

Project ini adalah aplikasi web portfolio berbasis Python Flask.
Fitur utama:

- Halaman utama portfolio dinamis dari TiDB
- Login admin
- Dashboard admin
- CRUD Profile
- CRUD Skill
- CRUD Experience
- CRUD Project
- CRUD Contact / pesan masuk
- Upload gambar ke Cloudinary
- Kirim email melalui Resend
- Konfigurasi menggunakan `.env` dan `os.getenv()`

## Cara Menjalankan

1. Buat virtual environment:

```powershell
python -m venv .venv
.venv\Scriptsctivate
```

2. Install dependency:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` menjadi `.env`, lalu isi data TiDB, Cloudinary, dan Resend.

4. Jalankan SQL `DB_NIM_NAMA.sql` di TiDB Cloud SQL Editor.

5. Test koneksi TiDB:

```powershell
python test_tidb.py
```

6. Jalankan Flask:

```powershell
python app.py
```

7. Buka halaman:

- Portfolio: http://127.0.0.1:5000/
- Admin Login: http://127.0.0.1:5000/admin/login

Default admin dari `.env.example`:

- Email: admin@gmail.com
- Password: admin123

## Catatan Pengumpulan

Rename file SQL menjadi format sesuai instruksi:

```txt
DB_NIM_NAMA.sql
```

Contoh:

```txt
DB_682024053_NAMA_KAMU.sql
```

Jangan upload file `.env` asli ke GitHub. Upload `.env.example` saja.
