FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN apt update && \
	apt-get install software-properties-common -y && \
	add-apt-repository ppa:alex-p/tesseract-ocr5 && \
    apt update && \
	apt install python3 python3-venv python3-pip python3-pil python3-opencv tesseract-ocr -y

WORKDIR /usr/src/app

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY work/requirements.txt ./
RUN pip install -Ur requirements.txt

COPY work/*.py ./

COPY entrypoint.sh ./
RUN chmod a+x entrypoint.sh
ENTRYPOINT ./entrypoint.sh