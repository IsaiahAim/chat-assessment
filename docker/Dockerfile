# Pull official base image 
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev

COPY ./app/requirements.txt ./requirements.txt
RUN pip install --upgrade cython
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt

# Copy entrypoint.sh
COPY ./docker/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

COPY ./app /app

ENTRYPOINT [ "/entrypoint.sh" ]