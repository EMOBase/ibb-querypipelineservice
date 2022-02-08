FROM python:3.8-alpine

WORKDIR /app

RUN adduser -D ibbtools

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
RUN chown -R ibbtools:ibbtools ./

USER ibbtools

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "wsgi:app"]
