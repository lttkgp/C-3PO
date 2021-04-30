# Base Python image for container
FROM python:3.7-slim
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

# Set unbuffered output to make sure all logs are printed and not stuck in buffer
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /c3po

# Copy and install requirements
ADD requirements /c3po/requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /c3po/requirements/common.txt && pip install --no-cache-dir -r /c3po/requirements/dev.txt

ADD . /c3po/
WORKDIR /c3po
RUN pip install -e .

ENV PYTHONPATH=/c3po

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
