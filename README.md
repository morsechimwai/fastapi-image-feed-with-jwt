# Image Feed API

A simple image feed application with FastAPI backend and Streamlit frontend

## Project Structure

```
.
├── backend/                 # Backend application
│   └── app/
│       ├── __init__.py
│       ├── main.py         # Start FastAPI application
│       ├── core/           # Configuration and main settings
│       │   ├── __init__.py
│       │   └── config.py   # Application settings
│       ├── db/             # Database configuration
│       │   ├── __init__.py
│       │   ├── base.py     # SQLAlchemy base
│       │   ├── session.py  # Database session management
│       │   ├── models.py   # Database models
│       │   └── init_db.py  # Initialize database
│       ├── models/         # Model exports (aliases)
│       │   └── __init__.py
│       ├── schemas/        # Pydantic schemas
│       │   ├── __init__.py
│       │   ├── user.py     # User schemas
│       │   └── post.py     # Post schemas
│       ├── api/            # API routes
│       │   ├── __init__.py
│       │   ├── deps.py     # API dependencies
│       │   └── v1/         # API version 1
│       │       ├── __init__.py
│       │       ├── auth.py    # Authentication endpoints
│       │       ├── users.py   # User endpoints
│       │       └── posts.py   # Post endpoints
│       ├── services/       # External services
│       │   ├── __init__.py
│       │   └── imagekit.py # ImageKit integration
│       └── users/          # User management
│           ├── __init__.py
│           └── manager.py  # User manager and authentication
├── frontend/               # Frontend application
│   ├── __init__.py
│   └── app.py             # Streamlit application
├── tests/                  # Test files
│   ├── __init__.py
│   └── conftest.py        # Pytest configuration
├── main.py                # Start application
├── pyproject.toml         # Project dependencies
├── env.example            # Example environment variables
└── README.md              # This file
```

## Features

- **Authentication**: JWT-based user authentication
- **Image/Video Upload**: Upload images and videos with ImageKit integration
- **Feed**: View all posts in feed format
- **User Management**: Register, login and manage user accounts
- **Post Management**: Create, view and delete posts

## Installation

### Prerequisites

- Python 3.13+
- ImageKit account (for file storage)
- `uv` package manager (recommended) or `pip`

### Installation

1. Clone repository:

```bash
git clone <repository-url>
cd fastapi-image-feed-api
```

2. Install dependencies:

```bash
uv sync
# or
pip install -e .
```

3. Create `.env` file from `env.example`:

```bash
cp env.example .env
```

4. Update `.env` with your configuration:

```env
SECRET=your-secret-key-here
IMAGEKIT_PUBLIC_KEY=your-imagekit-public-key
IMAGEKIT_PRIVATE_KEY=your-imagekit-private-key
IMAGEKIT_URL_ENDPOINT=your-imagekit-url-endpoint
DATABASE_URL=sqlite+aiosqlite:///./image-feed.sqlite3
```

## Run Application

### Backend (FastAPI)

```bash
python main.py
```

API will be available at `http://localhost:8888`
API documentation: `http://localhost:8888/docs`

### Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

Frontend will be available at `http://localhost:8501`

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/jwt/login` - Login and get JWT token
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/verify` - Verify email

### Users

- `GET /users/me` - View current user information
- `PATCH /users/me` - Update current user

### Posts

- `POST /upload` - Upload image or video
- `GET /feed` - View all posts in feed
- `DELETE /post/{post_id}` - Delete post

## Development

### Code Structure

This project follows best practices for FastAPI applications:

- **Separation of Concerns**: Clearly separate models, schemas, API routes and services
- **Dependency Injection**: Use dependency system of FastAPI
- **Type Safety**: Use Pydantic for data validation
- **Async/Await**: All database operations are async
- **Configuration Management**: Configuration management with Pydantic Settings

### Add New Features

1. **New API Endpoint**: add new API endpoint in `backend/app/api/v1/`
2. **New Model**: add new model in `backend/app/db/models.py`
3. **New Schema**: add new schema in `backend/app/schemas/`
4. **New Service**: add new service in `backend/app/services/`

## Contributing

ผมยังต้องฝึกอีกเยอะและโปรเจคนี้ก็ยังมีช่องว่างให้พัฒนาอีกมากครับ
หากคุณพบเห็นส่วนไหนที่สามารถปรับปรุงให้ดีขึ้นได้ — ไม่ว่าจะเล็กหรือใหญ่ — ยินดีรับทุกความช่วยเหลือจากทุก ๆ ท่านเลยครับ 🙏

ขั้นตอนร่วมสนับสนุน:

1. Fork repository
2. สร้าง branch ใหม่สำหรับการปรับปรุงของคุณ
3. ส่ง Pull Request พร้อมเล่าว่าคุณปรับปรุงอะไร อย่างไรบ้าง และทำไมถึงสำคัญ

ทุกการมีส่วนร่วม ทั้งโค้ด ไอเดีย หรือ feedback ช่วยให้โปรเจคนี้เติบโตเร็วขึ้นมากครับ
ขอบคุณที่มาช่วยกันสร้างสิ่งนี้ให้ดีขึ้นไปด้วยกันครับ 🩵

---

**🧑‍💻 Happy Hacking!**
