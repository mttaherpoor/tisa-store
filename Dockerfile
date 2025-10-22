FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

# upgrade pip
RUN python -m pip install --upgrade pip

# فقط requirements.txt را کپی می‌کنیم
COPY requirements.txt /code/

# نصب پکیج‌ها
RUN pip install --no-cache-dir -r requirements.txt

# سپس کل پروژه را کپی می‌کنیم
COPY . /code/
