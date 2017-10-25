FROM debian:stretch

RUN apt-get update && apt-get -y install build-essential curl python3 python-virtualenv libsphere-dev

RUN mkdir /tmp/audioseg

ADD Procfile /Procfile

RUN cd /tmp/audioseg &&\
    curl -s -O http://mirror.switch.ch/ftp/mirror/gnu/gsl/gsl-2.4.tar.gz &&\
    tar -xzf gsl-2.4.tar.gz &&\
    cd gsl-2.4 &&\
    sh ./configure &&\
    make && make install

RUN cd /tmp/audioseg &&\
    curl -s -O http://www.irisa.fr/metiss/guig/spro/spro-4.0.1/spro-4.0.1.tar.gz &&\
    tar -xzf spro-4.0.1.tar.gz &&\
    cd spro-4.0 &&\
    sh ./configure &&\
    make && make install

COPY utility/ssad.patch /tmp/audioseg/ssad.patch
RUN cd /tmp/audioseg &&\
    curl -s -O https://gforge.inria.fr/frs/download.php/file/31320/audioseg-1.2.2.tar.gz &&\
    tar -xzf audioseg-1.2.2.tar.gz &&\
    patch audioseg-1.2.2/src/ssad.c ssad.patch &&\
    cd audioseg-1.2.2 &&\
    sh ./configure &&\
    make && make install

RUN rm -r /tmp/audioseg/

ADD requirements.txt /requirements.pip
RUN cd / &&\
    virtualenv --python=python3 env &&\
    env/bin/pip install -r /requirements.pip gunicorn &&\
    rm /requirements.pip

EXPOSE 80/tcp
COPY application/ /application/
COPY  config/ /config

CMD /env/bin/gunicorn application:app --bind :80
