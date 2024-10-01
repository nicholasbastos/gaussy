FROM python:slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD [ "python3", "app.py" ]