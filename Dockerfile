FROM python:3.8-slim

ADD . /src

WORKDIR /src

RUN apt update \
 && apt install --no-install-recommends -y git \
 && pip install -r requirements.txt --no-cache-dir \
 && python setup.py develop \
 && apt remove -y git \
 && rm -rf /var/cache/* /var/lib/apt/lists/*

ENTRYPOINT ["aicrowd"]
