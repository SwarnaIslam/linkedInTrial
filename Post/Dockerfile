FROM python:3.10.12

WORKDIR /app/post

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

