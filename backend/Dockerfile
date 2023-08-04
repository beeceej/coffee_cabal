FROM python:3.11.4-slim-bookworm

RUN pip install pip-tools

ADD requirements.txt .
ADD dev-requirements.txt .

RUN pip-sync requirements.txt dev-requirements.txt

COPY . .

CMD uvicorn --host 0.0.0.0 app.api.main:app