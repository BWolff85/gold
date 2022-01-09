FROM python:3.7
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
# COPY core/ /usr/lib/python3.7/core/
# COPY . .

COPY . /web

WORKDIR /web
ENV PATH=$PATH:/web
ENV PYTHONPATH /web
RUN pip3 install -r requirements.txt
# RUN pip3 install flask
RUN pip3 install requests


ENTRYPOINT ["python"]
CMD ["app.py"]