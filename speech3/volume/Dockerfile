FROM python:3.8-slim
#FROM alpine:latest

RUN apt-get update \
  && apt-get install -y wget curl git \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* \

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki wymagane do pracy aplikacji
RUN git clone https://github.com/plainquery/python.git

#COPY python/speech3/requirements.txt ./
RUN ls -la
RUN cp python/speech3/python/requirements.txt .
#COPY python/speech3/main.py ./
RUN cp python/speech3/python/main.py .

RUN ls -la
#RUN wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
#RUN wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer
