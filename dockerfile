FROM python:3.10.6

RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /application
COPY docker-require.txt /application
RUN pip install --no-cache-dir --requirement /application/docker-require.txt
COPY . /application

CMD 'trigger.py'
