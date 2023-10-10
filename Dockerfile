FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# setup timezone
ENV TZ=Europe/Istanbul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update
RUN apt install -y wget software-properties-common python3-pip
RUN wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc
RUN add-apt-repository http://dl.openfoam.org/ubuntu
RUN apt-get update
RUN apt-get -y install openfoam9

RUN echo "source /opt/openfoam9/etc/bashrc" >> /root/.bashrc

RUN pip install poetry

COPY . .
RUN poetry export -f requirements.txt --output requirements.txt && pip3 install -r requirements.txt
