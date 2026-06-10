FROM python:3.11

WORKDIR /app

RUN pip install flask flask-mysqldb flask-cors gunicorn

COPY ./flask /app

EXPOSE 5001

CMD ["python", "app.py"]
