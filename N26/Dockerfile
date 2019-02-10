FROM python:2.7
RUN apt-get update -y
RUN apt-get install dnsutils vim -y
RUN apt-get install openssl -y
WORKDIR /usr/local/bin
COPY dns_over_tls_proxy.py .
CMD ["python","dns_over_tls_proxy.py"]
