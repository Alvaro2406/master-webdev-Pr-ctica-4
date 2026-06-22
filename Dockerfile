
FROM python:3.13  

RUN mkdir /app

WORKDIR /app

RUN pip install --upgrade pip 

COPY requirements.txt  /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && uvicorn just_globo.asgi:application --host 0.0.0.0 --port 8000"]