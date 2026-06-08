FROM python:3.11

WORKDIR /app

RUN pip install flask flask-mysqldb flask-cors

COPY ./flask /app

EXPOSE 5000

CMD ["python", "app.py"]