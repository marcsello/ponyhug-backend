FROM python:3.8-slim

ENV TZ Europe/Budapest
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

ARG RELEASE_ID
ENV RELEASE_ID ${RELEASE_ID:-""}

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ponyhug .

ENTRYPOINT ["python3", "application.py"]