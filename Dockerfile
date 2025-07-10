FROM --platform=linux/arm64/v8 python:3.9-slim-buster
COPY . /app

WORKDIR /app

COPY ./environment/env.main ./.env
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

CMD python Main.py