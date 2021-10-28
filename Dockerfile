FROM python:3.7

COPY . /home/klarna-solution
WORKDIR /home/klarna-solution


RUN pip install -r requirements.txt
