FROM python:latest


RUN mkdir -p /home/app

COPY . /home/app

WORKDIR /home/app

RUN pip install -r requirements.txt

CMD ["python3", "login.py"]
