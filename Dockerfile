FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# setup timezone
ENV TZ=Europe/Istanbul
ENV VM_PROJECT_DIR=/opt/openfoam11

# Create a non-root user 
RUN useradd -ms /bin/bash openfoamRunner

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update
RUN apt install -y wget software-properties-common python3-pip
RUN wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc
RUN add-apt-repository http://dl.openfoam.org/ubuntu
RUN apt-get update
RUN apt-get -y --no-install-recommends install openfoam11

RUN echo "source /opt/openfoam11/etc/bashrc" >> /root/.bashrc
RUN echo "source /opt/openfoam11/etc/bashrc" >> /home/openfoamRunner/.bashrc

RUN pip install poetry

# Change the ownership of your project directory to the non-root user
RUN chown -R openfoamRunner:openfoamRunner $VM_PROJECT_DIR

USER openfoamRunner

COPY . .
RUN poetry export -f requirements.txt --output /home/openfoamRunner/requirements.txt && pip3 install -r /home/openfoamRunner/requirements.txt

CMD ["/bin/bash"]

### POST-COMPILE (WIP) ###

# FROM ubuntu:22.04
# ENV DEBIAN_FRONTEND=noninteractive

# # setup timezone
# ENV TZ=Europe/Istanbul
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# RUN apt update
# RUN apt install -y wget software-properties-common python3-pip build-essential cmake flex openmpi-bin libopenmpi-dev
# RUN wget -O - https://dl.openfoam.org/gpg.key > /etc/apt/trusted.gpg.d/openfoam.asc
# RUN add-apt-repository http://dl.openfoam.org/ubuntu
# RUN apt-get update

# # Download and compile OpenFOAM 9 manually
# WORKDIR /opt
# RUN wget -O OpenFOAM-9.tar.gz http://dl.openfoam.org/source/9
# RUN mkdir OpenFOAM-9
# RUN tar -xzf OpenFOAM-9.tar.gz -C /opt/OpenFOAM-9 --strip-components=1
# WORKDIR /opt/OpenFOAM-9

# # Cleanup unnecessary files to reduce the image size
# RUN rm -rf /opt/OpenFOAM-9.tar.gz

# # Set up environment variables
# RUN echo "source /opt/OpenFOAM-9/etc/bashrc" >> /root/.bashrc

# # Build OpenFOAM
# RUN /bin/bash -c "source /opt/OpenFOAM-9/etc/bashrc && /opt/OpenFOAM-9/Allwmake"

# RUN pip install poetry

# WORKDIR /
# COPY . .
# RUN poetry export -f requirements.txt --output requirements.txt && pip3 install -r requirements.txt