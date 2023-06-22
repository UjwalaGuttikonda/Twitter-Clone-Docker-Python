FROM python:3.9-slim

RUN mkdir -p /home/

COPY ./home

RUN pip install --no-cache-dir -r requirements.txt

CMD["python","/home/main.py"]