FROM python:3.8-alpine

WORKDIR /app

RUN adduser -D ibbtools

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
COPY requirements.txt .

RUN python -m pip install --upgrade pip

# Build C extensions where no musllinux/arm wheel exists (notably PyYAML on
# Alpine arm64), then remove the compiler from the final image.
RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install -r requirements.txt \
    && apk del .build-deps

COPY . .
RUN chown -R ibbtools:ibbtools ./

USER ibbtools

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app"]
