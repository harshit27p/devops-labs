# Layer 1: Official lightweight Python runtime
FROM python:3.10-slim

# Layer 2: Metadata
LABEL maintainer="student@cdac.in"
LABEL service="flask-rest-api"

# Layer 3: Set working directory inside the container
WORKDIR /app

# Layer 4: Copy requirements first to leverage Docker layer caching
COPY requirements.txt .

# Layer 5: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Layer 6: Copy application code
COPY app.py .

# Layer 7: Expose Flask port
EXPOSE 5000

# Layer 8: Execute application on startup
CMD ["python", "app.py"]
