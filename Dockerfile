
# # Base image
# FROM python:3.11-slim

# Base image: upgraded for security
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt app.py boycott_list.csv ./
COPY templates/ ./templates
COPY static/ ./static

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# Upgrade pip to fix CVE-2025-8869 and install dependencies
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
