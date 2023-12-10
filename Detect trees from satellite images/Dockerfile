FROM python:3.10
ADD . .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD exec gunicorn app:server --bind :$PORT