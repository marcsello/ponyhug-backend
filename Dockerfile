FROM python:3.11-slim

ENV TZ Europe/Budapest
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

ARG SENTRY_RELEASE_ID
ENV SENTRY_RELEASE_ID ${SENTRY_RELEASE_ID:-""}

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ponyhug .

EXPOSE 8000

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "application:create_app()"]