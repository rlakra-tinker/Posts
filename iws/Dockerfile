# Multi-stage builds
# Layer - 1
FROM python:3.12 as builder

# Arguments
ARG APP_ENV=develop
ARG API_ENV=develop
ARG APP_NAME=iws_posts

# Define Env Variables
ENV APP_ENV="${APP_ENV}"
ENV API_ENV="${API_ENV}"
ENV APP_NAME="${APP_NAME}"

WORKDIR /app

COPY requirements.txt requirements.txt

# Virtual Env Setup
RUN python -m venv --upgrade-deps venv
# install dependencies to the working directory (eg. /app/)
RUN pip install --user -r requirements.txt
#RUN pip install -r requirements.txt
#RUN venv/bin/pip install -r requirements.txt

# Layer - 2
FROM python:3.12-slim as deploy

# Arguments
ARG APP_ENV=develop
ARG API_ENV=develop
ARG APP_NAME=iws_posts

# Define Env Variables
ENV APP_ENV="${APP_ENV}"
ENV API_ENV="${API_ENV}"
ENV APP_NAME="${APP_NAME}"

WORKDIR /app

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /app /app
COPY . /app

# update PATH environment variable
ENV PATH=/app/:$PATH

# EXPOSE is for documentation only - does not do anything
# 8082 is the default port the server is listening on
EXPOSE 8080
#HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 CMD  curl --silent --fail 0.0.0.0:8082/health_check || exit 1

# Add user
#RUN useradd app-user
#USER app-user
#COPY --chown=1000:1000 . app-user
#RUN pip install -e app-user
#COPY gunicorn.conf.py .
#USER app-user

# gunicorn -c gunicorn.conf.py wsgi:app
CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]
