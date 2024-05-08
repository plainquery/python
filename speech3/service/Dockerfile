FROM python:3.8-slim

RUN apt-get update
#RUN apt-get install -y python3-pyaudio portaudio19-dev python3-dev
RUN apt-get install -y python3-pyaudio portaudio19-dev
#fedora RUN dnf install -y portaudio-devel
RUN apt-get install -y wget curl

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki wymagane do pracy aplikacji
#COPY requirements.txt ./
#COPY main.py ./
#COPY deepspeech-0.9.3-models.pbmm ./
#COPY deepspeech-0.9.3-models.scorer ./
#RUN wget https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

# Zainstaluj potrzebne pakiety
RUN pip install --no-cache-dir -r requirements.txt

# Otwórz port 5000
EXPOSE 5000

# Uruchom aplikację
CMD ["python", "./main.py"]