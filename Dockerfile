#Lightweight Python base installation 
FROM python:3.9-slim

#Application directory
WORKDIR /app

#Update bare necessities 
RUN apt update && \
    apt install -y --no-install-recommends gcc libffi-dev

#Install dependencies 
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

#Copy app
COPY . .

#Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

#App port
EXPOSE 5000

#Run app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]