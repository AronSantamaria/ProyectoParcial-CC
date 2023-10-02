FROM python:3.10
WORKDIR /programas/website
RUN python -m pip install --upgrade pip
RUN pip install alembic==1.6.5
RUN pip install Flask==2.3.3
RUN pip install Flask-Migrate==3.0.1
RUN pip install Flask-SQLAlchemy==2.5.1
RUN pip install flask-restx==0.5.1
RUN pip install greenlet==1.1.0
RUN pip install itsdangerous==2.0.1
RUN pip install Mako==1.1.4
RUN pip install MarkupSafe==1.1.1
RUN pip install mysqlclient==2.0.3
RUN pip install psycopg2-binary
RUN pip install PyMySQL==1.0.2
RUN pip install python-dateutil==2.8.1
RUN pip install python-editor==1.0.4
RUN pip install six==1.16.0
RUN pip install werkzeug==2.0.3
RUN pip install flask-restx==0.5.1
RUN pip install SQLAlchemy==1.4.0
RUN pip install requests
RUN pip install bcrypt
COPY . . 
CMD [ "python3.10", "./app.py" ]