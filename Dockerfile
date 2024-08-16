FROM python:3.11-slim

RUN useradd -ms /bin/bash appuser
WORKDIR /home/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN ["touch", "log.txt"]
RUN ["chmod", "777", "log.txt"]

USER appuser

CMD python job.py & tail -f log.txt
