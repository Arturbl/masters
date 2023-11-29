FROM python:3.9

WORKDIR /app

COPY app.py /app
COPY db_handler_service.py /app
COPY payloaddto.py /app
COPY requirements.txt /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install requests

EXPOSE 8081

CMD ["python", "app.py"]
