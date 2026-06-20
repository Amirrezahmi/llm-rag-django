# سامانه پرسش از اسناد (LLM RAG Django)

یک سامانه هوشمند برای پرسش و پاسخ بر اساس اسناد، ساخته‌شده با Django، LangChain و ChromaDB.

لینک ویدئو کامل پروژه شامل توضیحات فنی و تئوریک، توضیح کد ها، setup پروژه، اجرای پروژه، دیدن نتایج، توضیح پنل همین و .. :

https://youtu.be/AswI1Yi9AeA?is=cc6odiIDxmhYb9xY

لینک ویدئو کوتاه صرفا برای توضیحات سریع، setup و اجرای سریع پروژه و آشنایی کلی با پنل ادمین:

https://youtu.be/oa_IIXWxLRw?is=T5mzDBdUAnjmUdcU


---

## فهرست مطالب

- [معرفی](#معرفی)
- [پیش‌نیازها](#پیش‌نیازها)
- [راه‌اندازی با Docker](#راه‌اندازی-با-docker)
- [راه‌اندازی بدون Docker](#راه‌اندازی-بدون-docker)
- [استفاده از سامانه](#استفاده-از-سامانه)
- [مستندات API](#مستندات-api)
- [ساختار پروژه](#ساختار-پروژه)
- [نکات فنی](#نکات-فنی)

---

## معرفی

این سامانه امکان بارگذاری اسناد متنی (فرمت `.docx`) و پرسش از محتوای آن‌ها را با استفاده از مدل زبانی فراهم می‌کند. سیستم با استفاده از RAG (Retrieval-Augmented Generation) بخش‌های مرتبط با سوال را از اسناد پیدا کرده و پاسخ دقیق تولید می‌کند.

**قابلیت‌ها:**
- افزودن، ویرایش و حذف اسناد
- پشتیبانی از فایل‌های `.docx`
- ذخیره متن کامل هر سند
- جستجوی معنایی در اسناد با ChromaDB
- تولید پاسخ با مدل زبانی از طریق OpenRouter
- ذخیره تاریخچه پرسش‌ها و پاسخ‌ها
- پنل مدیریت با Django Admin
- API کامل با Django REST Framework

---

## پیش‌نیازها

### برای اجرا با Docker:
- Docker
- Docker Compose
- یک API Key از [OpenRouter](https://openrouter.ai)

### برای اجرا بدون Docker:
- Python 3.11
- pip
- یک API Key از [OpenRouter](https://openrouter.ai)

---

## راه‌اندازی با Docker

### ۱. دریافت کد
```bash
git clone https://github.com/Amirrezahmi/llm-rag-django.git
cd llm-rag-django
```

یا فایل zip را استخراج کنید:
```bash
unzip llm-rag-django.zip
cd llm-rag-django
```

### ۲. تنظیم فایل `.env`

فایل `.env.example` را کپی کنید:
```bash
cp .env.example .env
```

سپس فایل `.env` را ویرایش کنید:
```bash
nano .env
```

محتوای فایل:
```env
SECRET_KEY=django-insecure-change-this-in-production-xyz123
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openrouter/auto

CHROMA_PERSIST_DIR=./chroma_db
```

> **توجه:** مقدار `OPENROUTER_API_KEY` را با API Key خود از سایت [openrouter.ai](https://openrouter.ai) جایگزین کنید.

### ۳. اجرا با Docker Compose

```bash
docker-compose up
```

سرور روی آدرس `http://localhost:8000` در دسترس خواهد بود.

برای اجرا در پس‌زمینه:
```bash
docker-compose up -d
```

برای متوقف کردن:
```bash
docker-compose down
```

---

## راه‌اندازی بدون Docker

### ۱. ساخت محیط مجازی

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### ۲. نصب پکیج‌ها

```bash
pip install -r requirements.txt
```

### ۳. تنظیم فایل `.env`

مطابق مرحله ۲ بخش Docker، فایل `.env` را بسازید.

### ۴. اجرای migration

```bash
python manage.py migrate
```

### ۵. ساخت superuser برای پنل مدیریت

```bash
python manage.py createsuperuser
```

### ۶. اجرای سرور

```bash
python manage.py runserver
```

سرور روی آدرس `http://127.0.0.1:8000` در دسترس خواهد بود.

---

## استفاده از سامانه

### پنل مدیریت

آدرس: `http://127.0.0.1:8000/admin`

با نام کاربری و رمزعبور superuser وارد شوید. در پنل می‌توانید:
- اسناد بارگذاری‌شده را مشاهده کنید
- تاریخچه پرسش‌ها و پاسخ‌ها را ببینید
- منابع استفاده‌شده برای هر پاسخ را مرور کنید

### بارگذاری سند

```bash
curl -X POST http://127.0.0.1:8000/api/documents/ \
  -F "title=عنوان سند" \
  -F "file=@/path/to/document.docx"
```

### پرسیدن سوال

```bash
curl -X POST http://127.0.0.1:8000/api/qa/ \
  -H "Content-Type: application/json" \
  -d '{"question_text": "سوال شما اینجا"}'
```

---

## مستندات API

### اسناد

| متد | آدرس | توضیح |
|-----|------|-------|
| GET | `/api/documents/` | دریافت لیست اسناد |
| POST | `/api/documents/` | بارگذاری سند جدید |
| GET | `/api/documents/{id}/` | دریافت جزئیات سند |
| PUT | `/api/documents/{id}/` | ویرایش سند |
| DELETE | `/api/documents/{id}/` | حذف سند |
| POST | `/api/documents/{id}/reindex/` | ایندکس مجدد سند |

### پرسش و پاسخ

| متد | آدرس | توضیح |
|-----|------|-------|
| GET | `/api/qa/` | دریافت تاریخچه پرسش‌ها |
| POST | `/api/qa/` | ثبت پرسش جدید و دریافت پاسخ |
| GET | `/api/qa/{id}/` | دریافت جزئیات یک پرسش |

#### نمونه درخواست بارگذاری سند:
```bash
curl -X POST http://127.0.0.1:8000/api/documents/ \
  -F "title=هوش مصنوعی" \
  -F "file=@ai_document.docx"
```

#### نمونه پاسخ:
```json
{
  "id": 1,
  "title": "هوش مصنوعی",
  "file": "http://127.0.0.1:8000/media/documents/ai_document.docx",
  "content": "متن کامل سند...",
  "is_indexed": true,
  "created_at": "2026-05-23T10:00:00+03:30",
  "updated_at": "2026-05-23T10:00:00+03:30"
}
```

#### نمونه درخواست پرسش:
```bash
curl -X POST http://127.0.0.1:8000/api/qa/ \
  -H "Content-Type: application/json" \
  -d '{"question_text": "هوش مصنوعی چیست؟"}'
```

#### نمونه پاسخ:
```json
{
  "id": 1,
  "question_text": "هوش مصنوعی چیست؟",
  "answer_text": "هوش مصنوعی هوشی است که توسط ماشین‌ها استفاده می‌شود...",
  "sources": [
    {
      "document_title": "هوش مصنوعی",
      "relevant_chunk": "بخش مرتبط از سند..."
    }
  ],
  "created_at": "2026-05-23T10:05:00+03:30"
}
```

---

## ساختار پروژه

```
llm-rag-django/
├── config/                 # تنظیمات Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── documents/              # اپ مدیریت اسناد
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── qa/                     # اپ پرسش و پاسخ
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── rag/                    # منطق RAG و LangChain
│   ├── extractor.py        # استخراج متن از docx
│   ├── indexer.py          # ایندکس‌گذاری در ChromaDB
│   └── chain.py            # زنجیره LangChain
├── media/                  # فایل‌های آپلودشده
├── chroma_db/              # پایگاه داده وکتور
├── packages/               # پکیج‌های offline
├── tiktoken_cache/         # کش tokenizer
├── .env                    # متغیرهای محیطی
├── requirements.txt        # پکیج‌های Python
├── Dockerfile
└── docker-compose.yml
```

---

## نکات فنی

### معماری RAG

۱. **استخراج متن:** فایل `.docx` آپلود می‌شود و متن با `python-docx` استخراج می‌شود.

۲. **تقسیم‌بندی متن:** متن به chunk های ۱۰۰۰ کاراکتری با overlap 200 کاراکتر تقسیم می‌شود.

۳. **ایندکس‌گذاری:** هر chunk با embedding از OpenRouter به ChromaDB اضافه می‌شود.

۴. **جستجو:** در زمان پرسش، سوال به embedding تبدیل شده و نزدیک‌ترین chunk ها پیدا می‌شوند.

۵. **تولید پاسخ:** chunk های مرتبط به مدل زبانی (از طریق OpenRouter) ارسال می‌شوند و پاسخ تولید می‌شود.

### مدل زبانی

از [OpenRouter](https://openrouter.ai) با مدل `openrouter/auto` استفاده می‌شود که به صورت خودکار بهترین مدل رایگان موجود را انتخاب می‌کند.

### محدودیت‌ها

- در حال حاضر فقط فایل‌های `.docx` پشتیبانی می‌شود.
- مدل‌های رایگان OpenRouter محدودیت ۵۰ درخواست در روز دارند.
- Docker به اینترنت برای ارتباط با OpenRouter نیاز دارد.

---

## دریافت API Key از OpenRouter

۱. به سایت [openrouter.ai](https://openrouter.ai) بروید.
۲. ثبت‌نام کنید (نیازی به کارت اعتباری نیست).
۳. از منو به **Keys** بروید.
۴. روی **Create Key** کلیک کنید.
۵. کلید ساخته‌شده را در فایل `.env` در مقابل `OPENROUTER_API_KEY` قرار دهید.

---

## نویسنده

امیررضا هاشمی
برای ارتباط با من به amirrezahmi2002@gmail.com ایمیل بدید.
