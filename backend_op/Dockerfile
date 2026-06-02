FROM python:3.13-bullseye

COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000