FROM ubuntu:20.04

RUN useradd -m -s /bin/bash pages_app

WORKDIR /home/pages_app

ADD requirements.txt requirements.txt

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    gcc python3-psycopg2 binutils libproj-dev gdal-bin python3-dev python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip3 install --upgrade pip \
  && pip3 install -r requirements.txt \
  && pip3 install gunicorn

ADD boot.sh boot.sh
RUN chmod +x boot.sh

RUN chown -R pages_app:pages_app ./
USER pages_app
WORKDIR /home/pages_app/pages_app

EXPOSE 8000
ENTRYPOINT ["../boot.sh"]
