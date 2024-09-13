FROM python:3.9

COPY . /app

WORKDIR /app

RUN apt-get update

RUN apt-get install -y tesseract-ocr tesseract-ocr-chi-sim

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "app:app"]
