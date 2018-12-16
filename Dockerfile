FROM python:3.7.1-alpine

COPY . .

RUN apk add --no-cache --virtual .build-deps build-base && \
    pip install -e .                                    && \
    apk del .build-deps

CMD [ "python", "-m", "pub" ]
