FROM python:3.9

ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql \
    postgresql-contrib \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /code/

# Set environment variables
ENV DATABASE_NAME=linkup
ENV DATABASE_USER=postgres
ENV DATABASE_PASSWORD=7156
ENV DATABASE_HOST=db
ENV DATABASE_PORT=5432

# Run migrations and start the Django server
RUN chmod +x ./start.sh
CMD ["./start.sh"]
