# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.8-slim

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Sets flask env to production so dev elements are removed
ENV FLASK_ENV=production

# Install mariadb client
RUN apt-get update && apt-get install -y \
    gcc \
    musl-dev \
    libmariadbclient-dev

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# install gunicorn
RUN python -m pip install gunicorn

RUN apt-get clean

WORKDIR /app
COPY backend /app/backend

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers=2", "backend:create_app()"]
