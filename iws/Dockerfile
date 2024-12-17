#FROM public.ecr.aws/docker/library/python:3.12.7-slim
#Specifies the Python base image.
FROM python:3.12-slim

# Arguments
ARG APP_ENV=develop
ARG API_ENV=develop

# Define Env Variables
ENV APP_ENV=$APP_ENV
ENV API_ENV=$API_ENV
#ENV APP_NAME=posts-iws

# Sets the working directory inside the Docker container at `/app`
WORKDIR /app

# Copies the current directory (.) from the host machine to the `/app` directory in the Docker container.
COPY . /app
#COPY requirements.txt .

# Installs the Python dependencies specified in the `requirements.txt` file.
RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

# Copy the rest of your application code into the container at /app
#COPY . .

# EXPOSE is for documentation only - does not do anything
# 8082 is the default port the server is listening on
EXPOSE 8080
#HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 CMD  curl --silent --fail 0.0.0.0:8082/health_check || exit 1

# gunicorn -c gunicorn.conf.py wsgi:app
#CMD ["gunicorn", "-c", "gunicorn.conf.py", "wsgi:app"]
#python -m flask --app wsgi run --port 8080 --debug
CMD ["python", "-m", "flask", "--app", "wsgi", "run", "--port=8080", "--host=0.0.0.0"]
