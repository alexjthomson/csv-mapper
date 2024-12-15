# syntax=docker/dockerfile:1

# Fetch the python 3 parent image. This image will be modified by adding a new
# `/code` directory. The parent image is further modified by installing the
# Python requirements defiend in `requirements.txt`:
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir /data
RUN chown 1000:1000 /data
RUN mkdir /log
RUN chown 1000:1000 /log

WORKDIR /code
COPY src/. /code/
RUN chown 1000:1000 /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN rm /code/requirements.txt

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]