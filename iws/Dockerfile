# Layer - 1
FROM python:3.12 as build
WORKDIR /opt
RUN python -m venv --upgrade-deps venv
COPY requirements requirements
RUN venv/bin/pip install -r requirements.txt
# Layer - 2
FROM python:3.12-slim as deploy
RUN useradd postuser
USER postuser
EXPOSE 8000
ENV PATH=/opt/venv/bin:$PATH \
    FLASK_APP=posts
USER root
COPY --from=build /opt/venv /opt/venv
WORKDIR /opt
COPY --chown=1000:1000 . postuser
RUN venv/bin/pip install -e postuser
COPY gunicorn_conf.py .
USER postuser
# gunicorn -c gunicorn.conf.py wsgi:app
CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]
