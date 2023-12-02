FROM python:3.9

WORKDIR /app

COPY requirements.txt /app
COPY src/processor.py /app
COPY src/db_handler_service.py /app
COPY src/csv_handler_service.py /app
COPY src/trainning.csv /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install requests

EXPOSE 8081

CMD ["python", "processor.py"]
