# Use Debian-based Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "list_service.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]
