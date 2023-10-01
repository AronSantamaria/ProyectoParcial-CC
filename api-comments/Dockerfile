FROM python:3.10
WORKDIR /programas/api-comments
RUN pip3 install flask
RUN pip install psycopg2
RUN pip install psycopg2-binary
RUN pip install flask_cors
COPY . .
CMD [ "python3", "./api.py" ]