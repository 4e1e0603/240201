FROM python:3.11-slim
RUN pip install pdm
WORKDIR /app
COPY . /app
