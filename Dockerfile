FROM python:3.8-slim

# Set environment variables
ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"

# Install system dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Copy requirements.txt into the working directory and install
COPY ./requirements.txt ./requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the rest of the application files into the working directory
COPY ./base ./base
COPY ./TextToMP3 ./TextToMP3
COPY ./manage.py ./manage.py
COPY ./migrations ./migrations
COPY ./static ./static
COPY ./templates ./templates

# Set app config option
ARG DJANGO_DEBUG
ENV DJANGO_DEBUG=$DJANGO_DEBUG

# Set argument vars in docker-run command
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION
ARG DJANGO_SECRET_KEY

# Set AWS cred env vars
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION
ENV DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY

CMD ["gunicorn", "-b", "0.0.0.0:8000", "TextToMP3.wsgi:application", "--log-level", "info", "--error-logfile", "-", "--workers=5"]
