# Todo List Application (FastAPI + MySQL + Vue 3)

## Deskripsi
Aplikasi **Todo List** lengkap dengan backend **FastAPI** (Python) dan frontend **Vue 3** (Vite).  
Implementasi mengikuti SRS‑TODO‑001 yang mencakup:
- CRUD Todo dengan pagination, sorting, filter, dan bulk‑generate.
- Health‑check endpoint.
- Dokumentasi API otomatis via Swagger UI.
- UI responsif dengan tema Dark Slate / Zinc.

---

## Prasyarat
| Komponen | Versi minimal | Cara instalasi |
|----------|----------------|----------------|
| **Python** | 3.12+ | `python -m venv .venv && .\.venv\Scripts\activate` |
| **Node.js / npm** | 20.x | Unduh dari https://nodejs.org/ |
| **MySQL** (opsional) | 8.0+ | Instal secara lokal atau gunakan SQLite (default) |
| **Git** | 2.40+ | `git --version` |

---

## Setup Backend
```powershell
# Pindah ke folder proyek (sudah di root)
cd C:\Users\ESZ GALLERY\Documents\Rofi\interview_task

# Buat virtual environment & aktifkan
python -m venv .venv
.\.venv\Scripts\activate

# Instal dependensi Python
pip install -r backend/requirements.txt
```

### Konfigurasi Database
- **SQLite (default)** – tidak perlu file `.env` khusus; file `todos.db` akan dibuat di `backend/`.
- **MySQL** – ubah nilai `DATABASE_URL` di `backend/.env`:
```
DATABASE_URL=mysql+aiomysql://<user>:<password>@<host>:3306/<dbname>
```
  Kemudian jalankan migrasi:
```powershell
alembic upgrade head
```

### Menjalankan Server
```powershell
python run.py   # menjalankan uvicorn dengan --app-dir backend
```
Server akan tersedia di **http://localhost:8000**.

---

## Setup Frontend
```powershell
cd frontend
npm ci   # atau npm install
```

### Mode Pengembangan (opsional)
```powershell
npm run dev   # Vite dev server pada http://localhost:5173
```

### Build Produksi
```powershell
npm run build   # hasil di frontend/dist, disajikan oleh FastAPI
```

---

## API Endpoint Ringkas
| Metode | Path | Deskripsi |
|--------|------|-----------|
| **GET** | `/api/v1/todos` | Daftar Todo (dapat pagination & filter) |
| **GET** | `/api/v1/todos/{id}` | Detail Todo |
| **POST** | `/api/v1/todos` | Buat Todo baru |
| **PUT** | `/api/v1/todos/{id}` | Update Todo |
| **DELETE** | `/api/v1/todos/{id}` | Hapus Todo |
| **POST** | `/api/v1/todos/bulk` | Generate random Todo (parameter `count`) |
| **GET** | `/api/v1/health` | Health check – mengembalikan `{"status":"healthy","database":"connected"}` |
| **GET** | `/docs` | Swagger UI (OpenAPI) |
| **GET** | `/redoc` | ReDoc UI |

---

## Cara Mengecek Health
```powershell
curl http://localhost:8000/api/v1/health
```
atau buka di browser **http://localhost:8000/api/v1/health**.

---

## Swagger UI
Buka di browser:
```
http://localhost:8000/docs
```
Menampilkan semua endpoint beserta contoh request/response.

---

## Deploy (opsional)
1. Pastikan variabel `DATABASE_URL` mengarah ke MySQL production.
2. Jalankan `alembic upgrade head` untuk migrasi.
3. Gunakan proses manager (systemd, PM2, Docker) untuk menjalankan `python run.py`.
4. Frontend sudah siap sebagai static files di `frontend/dist`.

---

## Kontribusi
1. Fork repositori ini.
2. Buat branch fitur: `git checkout -b feature/…`.
3. Push perubahan dan buat Pull Request.

---

## Lisensi
MIT License – lihat file `LICENSE` untuk detail.
