FROM debian:stretch

ADD requirements.txt /requirements.pip

RUN apt-get update && apt-get -y install build-essential curl python3 python-virtualenv libsphere-dev

RUN mkdir /home/segmentor

RUN cd /home/segmentor &&\
    curl -s -O http://mirror.switch.ch/ftp/mirror/gnu/gsl/gsl-2.4.tar.gz &&\
    tar -xzf gsl-2.4.tar.gz &&\
    cd gsl-2.4 &&\
    sh ./configure &&\
    make &&\
    make install

RUN cd /home/segmentor &&\
    curl -s -O http://www.irisa.fr/metiss/guig/spro/spro-4.0.1/spro-4.0.1.tar.gz &&\
    tar -xzf spro-4.0.1.tar.gz &&\
    cd spro-4.0 &&\
    sh ./configure &&\
    make &&\
    make install

COPY utility/ssad.patch /home/segmentor/ssad.patch
RUN cd /home/segmentor &&\
    curl -s -O https://gforge.inria.fr/frs/download.php/file/31320/audioseg-1.2.2.tar.gz &&\
    tar -xzf audioseg-1.2.2.tar.gz &&\
    patch audioseg-1.2.2/src/ssad.c ssad.patch &&\
    cd audioseg-1.2.2 &&\
    sh ./configure &&\
    make &&\
    make install

RUN cd / &&\
    virtualenv --python=python3 env &&\
    env/bin/pip install -r /requirements.pip gunicorn

RUN rm /requirements.pip
RUN rm -r /home/segmentor/*
