FROM python:3.6

ADD requirements.txt /requirements.txt
RUN cd / && \
    pip install -r /requirements.txt gunicorn && \
    rm /requirements.txt

COPY ./application/ /application
COPY ./config /config
