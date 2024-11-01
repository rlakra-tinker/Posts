# Layer - 1
FROM python:3.12 as build
WORKDIR /app
RUN python -m venv --upgrade-deps venv
COPY requirements requirements
RUN venv/bin/pip install -r requirements.txt

# Layer - 2
FROM python:3.12-slim as deploy
RUN useradd app-user
USER app-user
EXPOSE 8000
ENV PATH=/opt/venv/bin:$PATH \
    FLASK_APP=posts
USER root
COPY --from=build /opt/venv /opt/venv
WORKDIR /app
COPY --chown=1000:1000 . app-user
RUN venv/bin/pip install -e app-user
COPY gunicorn.conf.py .
USER app-user

# gunicorn -c gunicorn.conf.py wsgi:app
CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]
