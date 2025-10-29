# Base image
FROM python:3.12-slim

# جلوگیری از ایجاد فایل pyc و فعال کردن خروجی آنی
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# مسیر کاری
WORKDIR /code

# Upgrade pip
RUN python -m pip install --upgrade pip

# فقط requirements را کپی و نصب می‌کنیم
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# سپس کل پروژه را کپی می‌کنیم
COPY . /code/

# ایجاد دایرکتوری‌های media و protected_videos در کانتینر
RUN mkdir -p /var/www/media /var/protected_videos

# تغییر دسترسی (اختیاری، برای جلوگیری از Permission denied)
RUN chmod -R 777 /var/www/media /var/protected_videos