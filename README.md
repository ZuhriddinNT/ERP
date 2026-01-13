# EduRate - IT Learning Platform

EduRate bu IT o'quv markazlari uchun yaratilgan Teacher-Student Rating platformasi. Bu sistema student-larning teacher-larni baholash va o'z progressini kuzatish imkonini beradi.

## Xususiyatlar

### Student uchun:
- Kurslar ro'yxati va enrollment
- Teacher-larni baholash (5 yulduz sistema)
- Progress tracking
- Certificate management
- Pending ratings ko'rish

### Teacher uchun:
- Student-lardan feedback olish
- Rating breakdown (Teaching Quality, Course Content, Communication, Helpfulness, Punctuality)
- Student statistikasi
- Kurslarni boshqarish
- Analytics dashboard

## Texnologiyalar

- **Backend:** Django 4.2 (Pure Django, API yo'q)
- **Frontend:** TailwindCSS (CDN orqali)
- **Database:** SQLite
- **Authentication:** Django Built-in Auth

## O'rnatish

1. Virtual environment yarating:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

2. Dependencies o'rnating:
```bash
pip install -r requirements.txt
```

3. Database yarating:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Superuser yarating:
```bash
python manage.py createsuperuser
```

5. Serverni ishga tushiring:
```bash
python manage.py runserver
```

6. Brauzerda ochish:
```
http://localhost:8000
```

## Test ma'lumotlar yaratish

Admin panelga kiring va test student va teacher-lar yarating:
```
http://localhost:8000/admin
```

## Loyiha strukturasi

```
edurate_project/
├── edurate/                 # Main project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/                # User management
│   ├── models.py           # Custom User model
│   ├── views.py            # Login, Register, Dashboard
│   └── urls.py
├── courses/                 # Course management
│   ├── models.py           # Course, Enrollment
│   ├── views.py
│   └── urls.py
├── ratings/                 # Rating system
│   ├── models.py           # Rating model
│   ├── views.py
│   └── urls.py
├── templates/               # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── accounts/
│   ├── courses/
│   └── ratings/
├── static/                  # Static files
└── manage.py
```

## User Types

1. **Student** - Kurslarga yoziladi, teacher-larni baholaydi
2. **Teacher** - Kurslar yaratadi, feedback oladi

## Rating Criteria

1. Teaching Quality (O'qitish sifati)
2. Course Content (Kurs materiali)
3. Communication (Kommunikatsiya)
4. Helpfulness (Yordam berish)
5. Punctuality (Vaqtida kelish)

## Dashboard Features

### Student Dashboard:
- Enrolled courses
- Ratings given count
- Average progress
- Certificates
- Pending ratings

### Teacher Dashboard:
- Overall rating
- Total students
- Total ratings
- Active courses
- Rating breakdown
- Recent feedback

## License

MIT License
