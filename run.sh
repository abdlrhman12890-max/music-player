#!/bin/bash

# الخروج الفوري عند حدوث أخطاء غير متوقعة
set -e

echo "🔍 [1/5] جاري فحص وتثبيت التقنيات والأدوات على النظام..."

REQUIRED_PACKAGES=("python3" "python3-pip" "python3-venv" "ffmpeg" "nodejs" "curl")
MISSING_PACKAGES=()

for pkg in "${REQUIRED_PACKAGES[@]}"; do
    if ! dpkg -l | grep -q "^ii  $pkg "; then
        MISSING_PACKAGES+=("$pkg")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo "⚠️ تم كشف تقنيات مفقودة: ${MISSING_PACKAGES[*]}"
    echo "⚙️ جاري التثبيت تلقائياً..."
    sudo apt update
    sudo apt install -y "${MISSING_PACKAGES[@]}"
else
    echo "✅ جميع تقنيات النظام الأساسية مثبتة بنجاح."
fi

echo "🔍 [2/5] جاري إعداد وتفعيل البيئة الافتراضية (Virtual Environment)..."
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# تفعيل البيئة الافتراضية
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "../venv" ]; then
    source ../venv/bin/activate
else
    echo "⚙️ إنشاء بيئة افتراضية جديدة venv..."
    python3 -m venv venv
    source venv/bin/activate
fi

# التوجه تلقائياً إلى المجلد الذي يحتوي على manage.py
if [ ! -f "manage.py" ] && [ -d "music_project" ]; then
    cd music_project
fi

if [ ! -f "manage.py" ]; then
    echo "❌ خطأ: لم يتم العثور على ملف manage.py!"
    exit 1
fi

echo "🔍 [3/5] جاري فحص وتحديث مكتبات Python المطلوبة..."
pip install --upgrade pip > /dev/null
pip install --upgrade django yt-dlp > /dev/null

echo "🔍 [4/5] جاري فحص ومزامنة قاعدة البيانات (Database Migrations)..."
python3 manage.py makemigrations
python3 manage.py migrate

echo "------------------------------------------------------------------"
echo "🚀 [5/5] تم فحص وتجهيز جميع التقنيات بنجاح!"
echo "🌐 رابط الكمبيوتر: http://127.0.0.1:8000"
echo "📱 رابط الموبايل:  http://$(hostname -I | awk '{print $1}'):8000"
echo "------------------------------------------------------------------"

python3 manage.py runserver 0.0.0.0:8000