FROM ubuntu:latest

RUN apt update
RUN apt install python3-pip -y
WORKDIR /usr/app/src
COPY . ./
RUN pip3 install -r ./requirements.txt
COPY script.py ./

CMD [ "uvicorn", "script:app", "--host","0.0.0.0", "--reload" ]