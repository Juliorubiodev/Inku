# ---- Base image (Debian) ----
FROM python:3.11-bookworm

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# ---- Working directory ----
WORKDIR /app

# ---- Install dependencies ----
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---- Copy project ----
COPY . .

# ---- Expose port ----
EXPOSE 8000

# ---- Start FastAPI ----
CMD ["python", "-m", "uvicorn", "inku_api.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]
