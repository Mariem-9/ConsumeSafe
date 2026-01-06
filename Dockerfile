
# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt app.py boycott_list.csv ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
