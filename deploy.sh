#!/bin/bash

echo "🚀 جاري تجهيز وتشغيل سيرفر البلاير..."

# 1. تفعيل البيئة الافتراضية (إن كانت موجودة، أو إنشائها)
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 2. تثبيت المكتبات
pip install -r requirements.txt

# 3. تطبيق الـ Migrations وجمع الـ Static Files
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput

# 4. تشغيل السيرفر
echo "✅ تم التجهيز بنجاح! السيرفر يعمل الآن..."
python3 manage.py runserver 0.0.0.0:8000