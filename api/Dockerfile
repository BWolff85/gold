FROM python:3.7
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
# COPY core/ /usr/lib/python3.7/core/
# COPY . .

COPY . /api

WORKDIR /api
# ENV PATH=$PATH:/api
# ENV PYTHONPATH /api
RUN pip3 install -r requirements.txt
RUN pip3 install flask-mysqldb
RUN pip3 install mysql-connector-python
RUN pip install flask_sqlalchemy
Run pip install python-dotenv

ENTRYPOINT ["python"]
ENV PYTHONPATH="/:$PYTHONPATH"
CMD ["app.py"]