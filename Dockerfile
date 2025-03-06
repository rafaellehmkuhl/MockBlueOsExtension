FROM python:3.9-slim-buster

LABEL version="0.0.1"
LABEL permissions='[\
  {"permission": "networking", "reason": "Required for network communications"},\
  {"permission": "resources", "reason": "Required to manage system resources"},\
  {"permission": "register-service", "service": {"title":"Mock BlueOS Extension", "description": "A sample BlueOS extension", "path":"/frontend/index.html"}, "reason":"To appear in the BlueOS web interface"}\
]'
LABEL authors='[{"name": "Rafael Lehmkuhl", "email": "rafael.lehmkuhl93@gmail.com"}]'
LABEL company="BlueOS Extension Community"
LABEL title="Mock BlueOS Extension"
LABEL description="A sample BlueOS extension demonstrating basic functionality"
LABEL readme="https://raw.githubusercontent.com/rafaellehmkuhl/MockBlueOsExtension/main/README.md"
LABEL repository="https://github.com/rafaellehmkuhl/MockBlueOsExtension"
LABEL website="https://github.com/rafaellehmkuhl"
LABEL support="https://github.com/rafaellehmkuhl/MockBlueOsExtension/issues"

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy backend code and requirements
COPY src/backend /app/backend
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend files
COPY src/frontend /app/frontend

# Set default command
CMD ["python", "-m", "backend.main"]

# Expose port for the backend service
EXPOSE 8000