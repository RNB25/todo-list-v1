# Todo List v1

## Overview

A full‑stack Todo List application built with **FastAPI** (backend) and **Vue 3** (frontend). The project now uses **MySQL** (via XAMPP) as its database. The old SQLite file `todos.db` remains in the repository for legacy reference but is no longer used.

---

## Prerequisites

- **Python** >= 3.12
- **Node.js** >= 20 (npm comes with it)
- **XAMPP** with MySQL service running (default port `3306`)
- **Git** (for cloning the repo)

> **Note**: The MySQL `root` user is configured with **no password** as you requested. If you set a password, update the connection string accordingly.

---

## Project Structure

```
├─ backend/               # FastAPI source code
│   ├─ app/
│   ├─ migrations/        # Alembic migration scripts
│   └─ .env               # Environment variables (do not commit)
├─ frontend/              # Vue 3 source code
│   ├─ src/
│   └─ vite.config.ts
├─ todos.db               # Legacy SQLite DB (deprecated)
└─ README.md              # You are reading it now
```

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/RNB25/todo-list-v1.git
cd todo-list-v1
```

---

## 2️⃣ Backend Setup

### a. Create a virtual environment and install dependencies

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix/macOS (if needed)
# source venv/bin/activate
pip install -r backend/requirements.txt
```

### b. Configure the database connection

Create a `.env` file inside the `backend/` folder (copy the example if present):

```ini
# backend/.env
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/todo_db
# Optional: other env vars like SECRET_KEY, DEBUG, etc.
```

> The URL format is `dialect+driver://user:password@host:port/database`.

### c. Create the MySQL database

Open the **XAMPP MySQL console** (or any MySQL client) and run:

```sql
CREATE DATABASE IF NOT EXISTS todo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### d. Apply Alembic migrations (creates the tables)

```bash
cd backend
python -m alembic upgrade head
```

You should see output similar to:

```
INFO  [alembic.runtime.migration] Running upgrade  -> head, …
```

### e. Run the backend server

```bash
# From the backend directory
python run.py   # or:
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. Health endpoint:

```
GET /api/v1/health
```

You should receive JSON indicating `database: "connected"`.

---

## 3️⃣ Frontend Setup

```bash
cd ../frontend   # from the project root
npm install       # install dependencies
npm run dev       # start dev server (http://localhost:5173)
```

For a production build:

```bash
npm run build      # builds to frontend/dist/
npx serve -s dist   # simple static server (install serve globally if needed)
```

---

## 4️⃣ What is `todos.db`?

`todos.db` was the original **SQLite** database file used before the migration to MySQL. After switching to MySQL, the application no longer reads or writes to this file. You can safely delete it or keep it as a reference; it does **not** affect the running application.

---

## 5️⃣ Common Troubleshooting

| Issue | Likely Cause | Fix |
|-------|--------------|-----|
| **Cannot connect to MySQL** | MySQL service not running or wrong credentials | Start MySQL via XAMPP; ensure the connection string in `.env` matches your setup. |
| **Alembic fails** | Running command from wrong directory or missing `alembic.ini` | Execute `python -m alembic upgrade head` **inside** the `backend` folder. |
| **Backend health shows `database: "disconnected"`** | `.env` not loaded or wrong `DATABASE_URL` | Verify the `.env` file exists, has the correct URL, and restart the server. |
| **Frontend cannot reach API** | CORS mis‑configuration or wrong backend URL | Ensure the backend runs on `http://localhost:8000` and the frontend’s `VITE_API_URL` points there. |

---

## 6️⃣ License

[MIT License](LICENSE)

---

*Happy coding!*