FROM python:slim

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update

RUN apt install -y --no-install-recommends \
      bash \
      libnss3 \
      axel \
      ffmpeg \
      net-tools \
      redis-tools

RUN apt-get clean autoclean
RUN apt-get autoremove --yes
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

RUN mkdir /opt/py-yt-server
COPY app/requirements.txt /opt/py-yt-server
WORKDIR /opt/py-yt-server

RUN pip3 install -r requirements.txt

COPY app /opt/py-yt-server
