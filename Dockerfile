FROM python:3.10.14-alpine3.18

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN pip install -r requirements.txt

ENTRYPOINT python main.py --reload 


