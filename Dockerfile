FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /var/data/media

# collectstatic solo necesita SECRET_KEY; Cloudinary no se usa en build
ENV SECRET_KEY=build-placeholder USE_LOCAL_MEDIA=True MEDIA_ROOT=/var/data/media
RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["gunicorn", "curri.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
