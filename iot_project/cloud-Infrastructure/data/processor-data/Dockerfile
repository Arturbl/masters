FROM python:3.9

WORKDIR /app

COPY src/processor.py /app
COPY src/service/db_handler_service.py /app/service/db_handler_service.py
COPY src/service/csv_handler_service.py /app/service/csv_handler_service.py
COPY src/utils/trainning.csv /app/utils/trainning.csv
COPY requirements.txt /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install requests

EXPOSE 8081

CMD ["python", "processor.py"]
