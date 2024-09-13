FROM python:3.9

COPY . /app

WORKDIR /app

RUN apt-get update

RUN apt-get install -y tesseract-ocr tesseract-ocr-chi-sim libgl1

RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app"]
