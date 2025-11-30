# ---- Base image (Debian) ----
FROM python:3.11-bookworm

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

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
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
