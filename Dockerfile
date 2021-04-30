# Base Python image for container
FROM python:3.7-slim AS builder
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements/common.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


FROM python:3.7-slim

# Set unbuffered output to make sure all logs are printed and not stuck in buffer
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /c3po
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ADD . /c3po/
WORKDIR /c3po
RUN pip install -e .

ENV PYTHONPATH=/c3po

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
