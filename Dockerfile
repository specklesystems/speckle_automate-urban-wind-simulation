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

# Install necessary build tools and dependencies for OpenFOAM
RUN apt-get -y install build-essential cmake

# Download and compile OpenFOAM 9 manually
WORKDIR /opt
RUN wget -O OpenFOAM-v9.tar.gz https://github.com/OpenFOAM/OpenFOAM-9/archive/refs/tags/v9.tar.gz
RUN tar -xzf OpenFOAM-v9.tar.gz
WORKDIR /opt/OpenFOAM-9-v9
RUN source /etc/bash.bashrc && ./Allwmake

# Cleanup unnecessary files to reduce the image size
RUN rm -rf /opt/OpenFOAM-v9.tar.gz

# Set up environment variables
RUN echo "source /opt/OpenFOAM-9-v9/etc/bashrc" >> /root/.bashrc

RUN pip install poetry

COPY . .
RUN poetry export -f requirements.txt --output requirements.txt && pip3 install -r requirements.txt


# FROM ubuntu:22.04
# ENV DEBIAN_FRONTEND=noninteractive
# 
# # setup timezone
# ENV TZ=Europe/Istanbul
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
# 
# RUN apt update
# RUN apt install -y wget software-properties-common python3-pip
# RUN wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc
# RUN add-apt-repository http://dl.openfoam.org/ubuntu
# RUN apt-get update
# RUN apt-get -y --no-install-recommends install openfoam9
# 
# RUN echo "source /opt/openfoam9/etc/bashrc" >> /root/.bashrc
# 
# RUN pip install poetry
# 
# COPY . .
# RUN poetry export -f requirements.txt --output requirements.txt && pip3 install -r requirements.txt
