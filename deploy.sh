#!/bin/bash

# الخروج فوراً في حالة حدوث أي خطأ
set -e

echo "🚀 جاري تجهيز وتشغيل سيرفر البلاير..."

# 1. إنشاء البيئة الافتراضية بشكل طبيعي
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 2. تثبيت المكتبات باستخدام pip الخاص بالبيئة
./venv/bin/pip install -r requirements.txt

# 3. الدخول لمجلد المشروع
cd music_project

# 4. تنفيذ أوامر جانجو
../venv/bin/python3 manage.py makemigrations
../venv/bin/python3 manage.py migrate

# 5. تشغيل السيرفر
echo "✅ تم التجهيز بنجاح! السيرفر يعمل الآن على البورت 8000..."
../venv/bin/python3 manage.py runserver 0.0.0.0:8000