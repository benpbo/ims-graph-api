FROM python:3.10.5

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY flaskr /app

ENV FLASK_APP=flaskr

CMD [ "flask", "run" ]
