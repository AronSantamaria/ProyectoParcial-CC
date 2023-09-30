FROM python:3.10
WORKDIR /programas/api-preferences
RUN pip3 install flask
RUN pip install psycopg2
RUN pip install psycopg2-binary
COPY . .
CMD [ "python3", "./app.py" ]
