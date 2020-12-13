FROM python:3.8

WORKDIR /app
COPY src/main .
COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD [ "python", "rabbitmq.py" ]
