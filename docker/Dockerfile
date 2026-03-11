# Multi-stage build for production

# Backend stage
FROM python:3.10-slim as backend

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Frontend stage
FROM node:18-alpine as frontend

WORKDIR /app/frontend

COPY frontend/package.json .
RUN npm install

COPY frontend/ .
RUN npm run build

# Final stage
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY --from=backend /app/backend /app/backend
COPY --from=backend /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Copy frontend build
COPY --from=frontend /app/frontend/build /app/frontend/build

WORKDIR /app/backend

EXPOSE 5000

CMD ["python", "app.py"]
