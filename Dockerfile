FROM python:3

RUN apt-get update && apt-get install tesseract-ocr -y

WORKDIR /usr/src/app

COPY work/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY work/*.py ./

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

CMD [ "python", "./process.py" ]
