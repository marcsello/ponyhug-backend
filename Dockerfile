FROM python:3.11-slim

ENV TZ Europe/Budapest
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

ARG SENTRY_RELEASE_ID
ENV SENTRY_RELEASE_ID ${SENTRY_RELEASE_ID:-""}

COPY requirements.txt entrypoint.sh ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ponyhug .

EXPOSE 8000

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]