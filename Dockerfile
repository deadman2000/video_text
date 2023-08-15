FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive
ENV TZ UTC

RUN apt update && \
	apt-get install software-properties-common -y && \
	add-apt-repository ppa:alex-p/tesseract-ocr5 && \
    apt update && \
	apt install python3 python3-pip python3-pil python3-opencv tesseract-ocr -y

WORKDIR /usr/src/app

COPY work/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY work/*.py ./

CMD [ "python3", "./processor.py" ]